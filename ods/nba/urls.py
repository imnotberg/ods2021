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

]