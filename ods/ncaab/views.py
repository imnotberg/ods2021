from django.shortcuts import render
from django.http import JsonResponse
<<<<<<< HEAD
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
=======
from datetime import datetime
from .models import Date

# Create your views here.
def index(request):
	pass
def games(request,date_input):
	context = {'date_input':date_input}
	return render(request,'ncaab/games.html',context)
def games_feed(request,date_input):
	date = Date(date_input)
	return JsonResponse({"games":date.games,"info":date.info,},safe=False)

>>>>>>> 73a6c298e1a58d8476fcc6951515cc23eefe6407
