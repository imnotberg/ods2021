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
	teams = Teams(year)
	home_abbr = re.findall('([A-Z]+)',boxscore_index)[0]		
	home_sched = Schedule(home_abbr,year)
	home_gm = [t for t in home_sched if t.boxscore_index==boxscore_index][0].__dict__
	road_abbr = home_gm["_opponent_abbr"]
	road_tm = teams[road_abbr]
	road_sched = Schedule(road_abbr,year)
	home_sched_df = home_sched.dataframe
	road_sched_df = road_sched.dataframe
	road_gm = [t for t in road_sched if t.boxscore_index == boxscore_index][0].__dict__
	home_tm = teams[home_abbr].__dict__
	road_tm = teams[road_abbr].__dict__		
	date = datetime.strptime(boxscore_index[0:8],"%Y%m%d").strftime("%Y-%m-%d")
	road_record = road_sched_df[road_sched_df.datetime<datetime.strptime(date,"%Y-%m-%d")].to_json(orient="records")
	home_record = road_sched_df[road_sched_df.datetime<datetime.strptime(date,"%Y-%m-%d")].to_json(orient="records")
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
		away_players = None
		home_players = None
		game = None
		boxscore = None
	

	return JsonResponse({"boxscore":boxscore,"away_players":away_players,"home_players":home_players,"info":info,"odds":odds_dict,"road_tm":road_tm,"home_tm":home_tm,"road_sched":road_sched.dataframe.to_json(orient="records"),"home_sched":home_sched.dataframe.to_json(orient="records"),"road_record":road_record,"home_record":home_record,"home_gm":home_gm,"road_gm":road_gm,},safe=False)

def game(request,year,boxscore_index):
	context = {'year':year,'boxscore_index':boxscore_index}

	return render(request,'nba/game.html',context)