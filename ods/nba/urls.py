from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'nba'

urlpatterns = [
	path('',views.index,name='index'),
	path('teams-feed/year/<year>',views.teams_feed,name='teams_feed'),
	path('teams/year/<year>',views.teams,name='teams'),
	path('team-feed/<team_id>/year/<year>',views.team_feed,name='team_feed'),
	path('team/<team_id>/year/<year>',views.team,name='team'),
	path('game-feed/year/<year>/boxscore-index/<boxscore_index>',views.game_feed,name='game_feed'),
	path('game/year/<year>/boxscore-index/<boxscore_index>',views.game,name='game'),
	path('date-feed/date/<date_id>',views.date_feed,name='date_feed'),
	path('schedule/date/<date_id>',views.schedule_day,name='schedule'),
	path('test/game/year/<year>/boxscore-index/<boxscore_index>',views.test_game,name='test_game'),
	path('game-odds/year/<year>/boxscore-index/<boxscore_index>',views.game_odds,name="game_odds"),
	path('game-boxscore/year/<year>/boxscore-index/<boxscore_index>',views.game_boxscore,name="game_boxscore"),
	path('game-teams/year/<year>/boxscore-index/<boxscore_index>',views.game_teams,name="game_teams"),
]