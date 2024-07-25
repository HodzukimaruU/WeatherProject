import logging
import requests

from datetime import datetime
from typing import List, Dict, Optional

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Count

from .forms import CityForm
from .models import SearchHistory


logging.basicConfig(level=logging.DEBUG)

def get_coordinates(city_name: str) -> Optional[tuple[Optional[float], Optional[float]]]:
    api_key = '883103fe2eae495b8cc3574dbcd2b544'  # Замените на ваш API-ключ
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': city_name,
        'key': api_key,
        'limit': 1,
        'pretty': 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            print(f"No results found for {city_name}.")
            return None, None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None, None

def get_weather_data(city: str) -> Optional[List[Dict[str, any]]]:
    latitude, longitude = get_coordinates(city)
    if not latitude or not longitude:
        logging.error(f"Could not get coordinates for city: {city}")
        return None

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weather_code"],
        "timezone": "Europe/Moscow",
        "forecast_days": 7
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'daily' in data:
            daily_data = data['daily']
            weather_data = []
            num_days = len(daily_data['time'])
            
            for i in range(num_days):
                date_str = daily_data['time'][i]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_data = {
                    "date": date_obj.strftime('%A, %d %B %Y'),
                    "temperature_2m_max": daily_data['temperature_2m_max'][i],
                    "temperature_2m_min": daily_data['temperature_2m_min'][i],
                    "precipitation_sum": daily_data['precipitation_sum'][i],
                    "weather_code": daily_data['weather_code'][i]
                }
                weather_data.append(day_data)
            
            logging.debug(f"Weather data: {weather_data}")
            return weather_data
        else:
            logging.error("Daily data not found in the response")
            return None
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

def index(request: HttpRequest) -> HttpResponse:
    weather_data = None
    last_city = request.COOKIES.get('last_city', None)
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)
            if weather_data:
                SearchHistory.objects.create(city=city)
                response = render(request, 'weather/index.html', {'form': form, 'weather_data': weather_data})
                response.set_cookie('last_city', city)
                return response
            else:
                logging.error("Weather data is None")
    else:
        form = CityForm(initial={'city': last_city} if last_city else {})

    logging.debug(f"Weather data passed to template: {weather_data}")
    return render(request, 'weather/index.html', {'form': form, 'weather_data': weather_data})

def history(request: HttpRequest) -> HttpResponse:
    search_history = SearchHistory.objects.all().order_by('-search_date')
    return render(request, 'weather/history.html', {'search_history': search_history})

def autocomplete(request: HttpRequest) -> HttpResponse:
    if 'q' in request.GET:
        q = request.GET['q']
        cities = SearchHistory.objects.filter(city__istartswith=q).values_list('city', flat=True).distinct()[:10]
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)

def city_stats(request: HttpRequest) -> HttpResponse:
    stats = SearchHistory.objects.values('city').annotate(count=Count('city')).order_by('-count')
    return render(request, 'weather/city_stats.html', {'stats': stats})

def repeat_search(request: HttpRequest, city: str) -> HttpResponse:
    weather_data = get_weather_data(city)
    if weather_data:
        SearchHistory.objects.create(city=city)
        response = render(request, 'weather/repeat_search.html', {'city': city, 'weather_data': weather_data})
        response.set_cookie('last_city', city)
        return response
    else:
        logging.error("Weather data is None")
        return redirect('history')
