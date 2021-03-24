from django.shortcuts import render
from django.http import JsonResponse
from .models import Games
# Create your views here.

def index(request):
	pass

def games(request,date):
	context = {'date':date,}
	return render(request,'ncaab/games.html',context)

def games_feed(request,date=None):
	games = Games(date)
	game_list = games.games 
	info = games.info
	return JsonResponse({"games":game_list,"info":info,},safe=False)
