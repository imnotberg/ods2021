from django.http import JsonResponse
from django.shortcuts import render
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.schedule import Schedule 
from sportsreference.nfl.boxscore import Boxscore
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

def get_value(value):
	try:
		return value[0]
	except:
		return None
def index(request):
	context = {}

	return render(request,'nfl/index.html',context)

def teams_feed(request,year=datetime.now().year):
	all_teams = pd.concat([t.dataframe for t in Teams(year)]).sort_values(by=['rank'],ascending=True).to_json(orient="records")

	return JsonResponse(all_teams,safe=False)

def teams(request,year=datetime.now().year):
	context = {
		'year':year,
	}
	return render(request,'nfl/teams.html',context)

def team_feed(request,team_id,year=datetime.now().year):
	team = Teams(year)[team_id].dataframe.to_json(orient="records")
	schedule = Schedule(team_id,year).dataframe.to_json(orient="records")
	data = {"info":team,"schedule":schedule,}
	return JsonResponse(data,safe=False)

def team(request,team_id,year=datetime.now()):

	context = {'year':year,'team_id':team_id,}
	
	return render(request,'nfl/team.html',context)

def game_feed(request,year,boxscore_index):
	teams = Teams(year)
	home_abbr = re.findall('([A-Za-z]+)',boxscore_index)[0]		
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
	url = f"https://www.covers.com/sports/nfl/matchups?selectedDate={date}"
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

def game(request,year,team_abbr,boxscore_index):
	context = {'year':year,'boxscore_index':boxscore_index}

	return render(request,'nfl/game.html',context)

def date_feed(request,date_id):
	year = date_id[0:4]
	month = datetime.strptime(date_id,"%Y%m%d").strftime("%B").lower()
	url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
	page = requests.get(url)
	tree = html.fromstring(page.text)	
	feed = {get_value(t.xpath('.//th[@data-stat="date_game"]/@csk')):{"game_id":get_value(t.xpath('.//th/@csk')),"road_team":get_value(t.xpath('.//td[@data-stat="visitor_team_name"]//a/text()')),"road_points":get_value(t.xpath('.//td[@data-stat="visitor_pts"]/text()')),"home_team":get_value(t.xpath('.//td[@data-stat="home_team_name"]//a/text()')),"home_points":get_value(t.xpath('.//td[@data-stat="home_pts"]/text()'))} for t in tree.xpath('//table[@id="schedule"]//tbody//tr')} 
	games = {game:game_info for game,game_info in feed.items() if date_id in game}
	context = {"games":games,}
	return JsonResponse(context,safe=False)

def schedule_day(request,date_id):
	year = date_id[0:4]
	month = datetime.strptime(date_id,"%Y%m%d").strftime("%B").lower()
	url = f"https://www.pro-football-reference.com/years/{year}/games.htm"

	page = requests.get(url)
	tree = html.fromstring(page.text)	
	feed = {get_value(t.xpath('.//th[@data-stat="date_game"]/@csk')):{"game_id":get_value(t.xpath('.//th/@csk')),"road_team":get_value(t.xpath('.//td[@data-stat="visitor_team_name"]//a/text()')),"road_points":get_value(t.xpath('.//td[@data-stat="visitor_pts"]/text()')),"home_team":get_value(t.xpath('.//td[@data-stat="home_team_name"]//a/text()')),"home_points":get_value(t.xpath('.//td[@data-stat="home_pts"]/text()'))} for t in tree.xpath('//table[@id="schedule"]//tbody//tr')} 
	games = df.from_dict({game:game_info for game,game_info in feed.items() if date_id in game},orient='index')
	context = {"games":games,"year":year,}
	return render(request,'nba/schedule.html',context)


