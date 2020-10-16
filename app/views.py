from django.shortcuts import render
import requests
from .models import City
from .forms import CityForms
def index(request):
	url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f284336c73ff663a49db5c1a4434e634"
	if(request.method=="POST"):
		form=CityForms(request.POST)
		r=requests.get(url.format(request.POST['name'])).json()
		if(r['cod']=='404'):
			pass
		else:
			form.save()
		
	form = CityForms()

	cities=City.objects.all()
	data=[]
	for city in cities:
		r=requests.get(url.format(city)).json()
		details={
			"city":city.name.capitalize(),
			"description":r["main"]["temp"],
			"tempreature":r["weather"][0]["description"],
			"icon":r["weather"][0]["icon"],
		}
		data.append(details)
	
	context={"data":data ,"form":form}
	return render(request,'weather/weather.html',context)
