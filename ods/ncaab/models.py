from django.db import models
from sportsreference.ncaab.boxscore import Boxscore,Boxscores
from datetime import datetime
from lxml import html
import requests, re 
# Create your models here.
class Team(models.Model):
	name = models.CharField(max_length=200)
	conference = models.CharField(max_length=200,null=True)
	abbreviation = models.CharField(max_length=200,null=True)

	def __str__(self):
		return f"{self.name}"
	#def get_absolute_url(self):
		#pass
	@property
	def _reverse_lookup(self):
		return self.__reverse_lookup
	
class Games:
	def __init__(self,date_input=None):
		if date_input == None:
			date = datetime.now()
		else:
			date = datetime.strptime(date_input,"%Y%m%d")
		datestring = date.strftime("%#m-%#d-%Y")
		self.games = Boxscores(date).games[datestring]
		self.info = get_info('ncaab',date_input)

def get_info(league,date_input):
	date = datetime.strptime(date_input,"%Y%m%d").strftime("%Y-%m-%d") 
	url = f"https://www.covers.com/sports/{league}/matchups?selectedDate={date}"
	page = requests.get(url)
	tree = html.fromstring(page.text)
	games_dict = [{"away_team":f"{g.xpath('./@data-away-team-fullname-search')[0]} {g.xpath('./@data-away-team-nickname-search')[0]}" ,"away_conference":get_value(g.xpath('./@data-away-conference')),"home_team":f"{g.xpath('./@data-home-team-fullname-search')[0]} {g.xpath('./@data-home-team-nickname-search')[0]}","home_conference":get_value(g.xpath('./data-home-conference')),"away_score":get_value(g.xpath('./@data-away-score')),"home_score":get_value(g.xpath('./@data-home-score')),"odds":g.xpath('./@data-game-odd')[0],"total":g.xpath('./@data-game-total')[0],"datetime":get_value(g.xpath('./@data-game-date'))} for g in tree.xpath('//div[@class="cmg_matchup_game_box cmg_game_data"]')]
	return games_dict

def get_value(value):
	try:
		return value[0]
	except:
		return None

