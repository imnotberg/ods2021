from django.http import JsonResponse
from django.shortcuts import render
from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule 
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
from pandas import DataFrame as df
import json,requests,re
from lxml import html
from datetime import datetime

# Create your views here.
def extract_html(value):
	try:
		return value.text()
	except:
		return value
def index(request):
	context = {}

	return render(request,'nba/index.html',context)

def teams_feed(request,year=datetime.now().year):
	all_teams = pd.concat([t.dataframe for t in Teams(year)]).sort_values(by=['rank'],ascending=True).to_json(orient="records")

	return JsonResponse(all_teams,safe=False)

def teams(request,year=datetime.now().year):
	context = {
		'year':year,
	}
	return render(request,'nba/teams.html',context)

def team_feed(request,team_id,year=datetime.now().year):
	team = Teams(year)[team_id].dataframe.to_json(orient="records")
	schedule = Schedule(team_id,year).dataframe.to_json(orient="records")
	data = {"info":team,"schedule":schedule,}
	return JsonResponse(data,safe=False)

def team(request,team_id,year=datetime.now()):

	context = {'year':year,'team_id':team_id,}
	
	return render(request,'nba/team.html',context)

def game_feed(request,year,boxscore_index):
	team_abbr = re.findall('([A-Z]+)',boxscore_index)[0]
	year = boxscore_index[0:4]
	team_sched = Schedule(team_abbr,year)
	date = datetime.strptime(boxscore_index[0:8],"%Y%m%d").strftime("%Y-%m-%d")
	url = f"https://www.covers.com/sports/nba/matchups?selectedDate={date}"
	page = requests.get(url)
	tree = html.fromstring(page.text)
	odds_dict = {g.xpath('./@data-event-id')[0]:{"away_team":f"{g.xpath('./@data-away-team-fullname-search')[0]} {g.xpath('./@data-away-team-nickname-search')[0]}" ,"home_team":f"{g.xpath('./@data-home-team-fullname-search')[0]} {g.xpath('./@data-home-team-nickname-search')[0]}","odds":g.xpath('./@data-game-odd')[0],"total":g.xpath('./@data-game-total')[0],} for g in tree.xpath('//div[@class="cmg_matchup_game_box cmg_game_data"]')}
	try:	
		game = Boxscore(boxscore_index)
		info = json.dumps({k:extract_html(v) for k,v in game.__dict__.items() if 'players' not in k})
		boxscore = game.dataframe.to_json(orient="records")
		away_players = pd.concat([df.from_dict(p.__dict__,orient="index").T for p in game.away_players]).to_json(orient="records")
		home_players = pd.concat([df.from_dict(p.__dict__,orient="index").T for p in game.home_players]).to_json(orient="records")
	except:
		away_players = {}
		home_players = {}
		game = {}
		boxscore = {}
	

	return JsonResponse({"boxscore":boxscore,"away_players":away_players,"home_players":home_players,"info":info,"odds":odds_dict,},safe=False)

def game(request,year,boxscore_index):
	context = {'year':year,'boxscore_index':boxscore_index}

	return render(request,'nba/game.html',context)