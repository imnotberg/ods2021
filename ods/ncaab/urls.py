from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'ncaab'

urlpatterns = [
	path('',views.index,name='index'),
<<<<<<< HEAD
	path('games/date/<date>',views.games,name='games'),
	path('games-feed/date/<date>',views.games_feed,name='games_feed'),
]
=======
	path('games/date/<date_input>',views.games,name='games'),
	path('games-feed/date/<date_input>',views.games_feed,name="games_feed"),
	]
>>>>>>> 73a6c298e1a58d8476fcc6951515cc23eefe6407
