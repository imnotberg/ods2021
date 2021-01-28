from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'mlb'

urlpatterns = [
	path('',views.index,name='index'),
	path('teams-feed/year/<year>',views.teams_feed,name='teams_feed'),
	path('teams/year/<year>',views.teams,name='teams'),
	path('team-feed/<team_id>/year/<year>',views.team_feed,name='team_feed'),
	path('team/<team_id>/year/<year>',views.team,name='team'),
	path('game-feed/year/<year>/boxscore-index/<team_abbr>/<boxscore_index>',views.game_feed,name='game_feed'),
	path('game/year/<year>/boxscore-index/<team_id>/<boxscore_index>',views.game,name='game'),
	path('date-feed/date/<date_id>',views.date_feed,name='date_feed'),
	path('schedule/date/<date_id>',views.schedule_day,name='schedule'),
	

]