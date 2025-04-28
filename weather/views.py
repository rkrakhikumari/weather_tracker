from django.shortcuts import render
import requests
from datetime import datetime

def index(request):
    weather_data = {}
    forecast_data = []
    city = ""

    if request.method == 'POST':
        if 'clear' in request.POST:
            weather_data = {}
            forecast_data = []
            city = ""
        else:
            city = request.POST.get('city')
            api_key = '82045b40a0e005f3e1486bf9e26bb49d'

            # First, get latitude and longitude of city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    lat = data['coord']['lat']
                    lon = data['coord']['lon']

                    # Get 7-day forecast
                    forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely,current,alerts&appid={api_key}&units=metric"
                    forecast_response = requests.get(forecast_url)
                    if forecast_response.status_code == 200:
                        forecast_json = forecast_response.json()
                        for day in forecast_json['daily'][:7]:
                            date = datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
                            forecast_data.append({
                                'date': date,
                                'temp_day': day['temp']['day'],
                                'weather': day['weather'][0]['description'],
                                'wind_speed': day['wind_speed'],
                                'icon': day['weather'][0]['icon'],
                            })

                    weather_data = {
                        'city': city,
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'wind_speed': data['wind']['speed'],
                    }
                else:
                    weather_data['error'] = "City not found. Please try again."
            except Exception as e:
                weather_data['error'] = "Something went wrong: " + str(e)

    return render(request, 'weather/home.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'city': city
    })


