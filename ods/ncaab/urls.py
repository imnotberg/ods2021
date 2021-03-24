from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'ncaab'

urlpatterns = [
	path('',views.index,name='index'),
	path('games/date/<date>',views.games,name='games'),
	path('games-feed/date/<date>',views.games_feed,name='games_feed'),
]