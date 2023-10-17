import os
import requests
import json
from http import HTTPStatus
from datetime import datetime, timedelta, timezone
from custom_exceptions import *
from weather_dataclass import CurrentWeather

class WeatherClient:
    API_key : str = "7bd479633f081dc9d67691e3afa0fa36"
    API_adress : str = "http://api.openweathermap.org/data/2.5/weather"
    history_directory : str = os.path.dirname(os.path.dirname(__file__)) + '\\logfiles\\'

    def get_weather(self, place : str) -> CurrentWeather:
        if place == 'Мое местоположение':
            try:
                my_location = self.__get_location()
            except:
                raise LocationException
            else:
                request_json = self.__make_geolocation_weather_request(my_location)
        else:
            request_json = self.__make_city_weather_request(place)

        request_status = int(request_json['cod'])

        match request_status:
            case HTTPStatus.NOT_FOUND:
                raise InvalidInputException
            case HTTPStatus.BAD_REQUEST:
                raise EmptyInputException
            case HTTPStatus.UNAUTHORIZED | HTTPStatus.FORBIDDEN:
                raise APIRequestException
            case HTTPStatus.OK:
                return self.__generate_weather_report(request_json)
            case _:
                raise Exception


    def log_to_history(self, report : CurrentWeather) -> None:
        path = self.history_directory + "history.json"
        if not self.__history_exists(path) or self.__is_history_empty(path):
            with open(path, 'a+') as file:
                history_objects = []
                history_objects.append(report.to_JSON())
                json.dump(history_objects, file, indent=3)
        else:
            with open(path, 'r+') as file:
                history_objects = json.load(file)
                history_objects.append(report.to_JSON())
                file.seek(0)
                json.dump(history_objects, file, indent=3)


    def get_history(self) -> list:
        path = self.history_directory + "history.json"
        if self.__history_exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        else:
            with open(path, 'a') as file:
                file.write('')
            return "Истории пока нет"
        
        
    def clear_history(self) -> None:
        path = self.history_directory + "history.json"
        with open(path, 'w') as file:
            pass

    def __make_city_weather_request(self, place : str) -> dict:
        weather_request = requests.get(self.API_adress, 
                        params={'q': place, 'units': 'metric', 'lang': 'ru', 'APPID': self.API_key})
        return weather_request.json()
    
    def __make_geolocation_weather_request(self, place : tuple) -> dict:
        weather_request = requests.get(self.API_adress, 
                        params={'lat': place[0], 'lon': place[1], 'units': 'metric', 'lang': 'ru', 'APPID': self.API_key})
        return weather_request.json()
    
    def __get_location(self) -> tuple:
        response = requests.get('http://ipinfo.io/json').json()
        location = response['loc'].split(',')
        latitude = float(location[0])
        longitude = float(location[1])
        return (latitude, longitude)
    
    def __generate_weather_report(self, weather_request_json : dict) -> CurrentWeather:
        timezone = int(weather_request_json['timezone'])
        date_and_time = self.__calculate_time(timezone)
        datetime_to_string = date_and_time.strftime("%Y-%d-%m %H:%M:%S %Z")
        weather_data = CurrentWeather(
            time = datetime_to_string,
            place = weather_request_json['name'],
            weather = weather_request_json['weather'][0]['description'],
            real_temperature = int(weather_request_json['main']['temp']),
            feels_like_temparature = int(weather_request_json['main']['feels_like']),
            wind_speed = weather_request_json['wind']['speed']
        )
        return weather_data

    def __calculate_time(self, seconds_shift_from_UTC : int) -> datetime:
        tmzn = timezone(timedelta(seconds=seconds_shift_from_UTC))
        return datetime.now(tz = tmzn)

    def __history_exists(self, path: str) -> bool:
        return os.path.isfile(path)
    
    def __is_history_empty(self, path: str) -> bool:
        return os.path.getsize(path) == 0
    