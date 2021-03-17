from django.db import models
from sportsreference.ncaab.boxscore import Boxscores,Boxscore
from datetime import datetime, timedelta
from lxml import html
import requests, re,json
# Create your models here.
def get_value(value):
	try:
		return value[0]
	except:
		return None
class Team(models.Model):
	name = models.CharField(max_length=200)
	abbreviation = models.CharField(max_length=200)
	conference = models.CharField(max_length=200)

class Date:
	def __init__(self,date_input=None):
		if date_input == None:
			date = datetime.now()
		else:
			date = datetime.strptime(date_input,"%Y%m%d")
		url = f"https://www.covers.com/sports/ncaab/matchups?selectedDate={date}"
		page = requests.get(url)
		tree = html.fromstring(page.text)
		dictionary_date = f"{date.month}-{date.day}-{date.year}"
		self.date = date
		self.games = Boxscores(date).games[dictionary_date]
		self.info = [{"datetime":get_value(g.xpath('./@data-game-date')),"away_team":f"{g.xpath('./@data-away-team-fullname-search')[0]} {g.xpath('./@data-away-team-nickname-search')[0]}" ,"away_conference":get_value(g.xpath('./@data-away-conference')),"home_team":f"{g.xpath('./@data-home-team-fullname-search')[0]} {g.xpath('./@data-home-team-nickname-search')[0]}","home_conference":get_value(g.xpath('./@data-home-conference')),"odds":g.xpath('./@data-game-odd')[0],"datetime":get_value(g.xpath('./@data-game-date')),"home_score":get_value(g.xpath('./@data-home-score')),"away_score":get_value(g.xpath('./@data-away-score')),"total":get_value(g.xpath('./@data-game-total')),} for g in tree.xpath('//div[@class="cmg_matchup_game_box cmg_game_data"]') + tree.xpath('//div[@class="cmg_matchup_game_box  cmg_game_data"]')]



