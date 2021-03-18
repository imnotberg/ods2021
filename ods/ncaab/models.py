from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
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
class Pick:
	def __init__(self,user,date,week,league,value,game,team,opp,line,total):
		self._user = user
		self._league = league
		self._game = game
		self._value = value
		self._team = team
		self._opp = opp
		self._line = line
		self._total = total
		self.pick_time = datetime.now().strftime("%Y%m%d%H%M%S")
		self.result = None
		self.account = None
		self.all = {f"{self.user}{self.game}":{x:y for x,y in self.__dict__.items()}}

		def save_to_picks(self):
			picks,created = Picks.objects.get_or_create(pk=1)
			picks.picks.append(self.all)
			picks.save()
		save_to_picks(self)

	@property
	def user(self):
		return self._user

	@property
	def league(self):
		return self._league
	@property
	def game(self):
		return self._game
	@property
	def value(self):
		return self._value
	@property
	def team(self):
		return self._team
	@property
	def opp(self):
		return self._opp
	@property
	def line(self):
		return self._line
	@property
	def total(self):
		return self._total	 

class Picks(models.Model):
	picks = PickledObjectField(null=True)
class Profile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user.username}"

	def get_absolute_url(self):
		return reverse(':profile_detail',kwargs={'pk':self.pk})


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



