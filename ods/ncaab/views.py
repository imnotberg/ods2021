from django.shortcuts import render
from django.http import JsonResponse
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

