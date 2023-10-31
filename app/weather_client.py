import os
import requests
import geocoder
from http import HTTPStatus
from datetime import datetime, timedelta, timezone
from custom_exceptions import *
from weather_dataclass import Weather
from storage import Storage


STATUS_TO_ERROR = {
    HTTPStatus.NOT_FOUND : InvalidInputError,
    HTTPStatus.BAD_REQUEST : EmptyInputError,
    HTTPStatus.UNAUTHORIZED : APIRequestError,
    HTTPStatus.FORBIDDEN : APIRequestError
}


class WeatherClient:
    api_key : str = "7bd479633f081dc9d67691e3afa0fa36"
    api_adress : str = "http://api.openweathermap.org/data/2.5/weather"
    history_file : str = 'history.json'
    storage : Storage = Storage(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'logfiles'
            )
        )


    def get_weather(self, place : str) -> Weather:
        '''
        Основной метод клиента.
        На вход получает -me или имя населенного пункта.
        В случае удачного запроса возврвщает экземпляр датакласса Weather с информацией о погоде в 
        запрошенном населенном пункте.
        В случае неудачного запроса райзит ошибки в зависимости от причины неудачи.
        '''
        if place == '-me':
            try:
                place = WeatherClient.__get_location()
            except:
                raise LocationError          
        
        request_json = self.__make_city_weather_request(place)
        request_status = int(request_json['cod'])

        if request_status in STATUS_TO_ERROR:
            raise STATUS_TO_ERROR[request_status]
        elif request_status == HTTPStatus.OK:
            return WeatherClient.__generate_weather_report(request_json)
        else:
            raise Exception


    def log_to_history(self, report : Weather) -> None:
        '''Записывает в JSON-файл данные о погоде, представленные экземпляром датакласса'''
        self.storage.log_to_json(self.history_file, report.to_dict())      


    def get_history(self) -> list[dict]:
        '''Возвращает список со словарями данных о погоде'''
        return self.storage.read_from_json(self.history_file)


    def clear_history(self) -> None:
        '''Метод очищает файл с историей'''
        self.storage.clear_file(self.history_file)


    def __make_city_weather_request(self, place : str) -> dict:
        '''
        Метод совершает запрос к сервису Openweather по имени населенного пункта
        Возвращается JSON-файл с результатами запроса
        '''
        weather_request = requests.get(
            self.api_adress, 
            params = {'q': place, 'units': 'metric', 'lang': 'ru', 'APPID': self.api_key}
            )
        return weather_request.json()
    

    @staticmethod
    def __get_location() -> str:
        '''
        Метод возвращает имя вашего населенного пункта по IP
        '''
        me = geocoder.ip('me')
        city = me.city
        return city
    

    @staticmethod
    def __generate_weather_report(weather_request_json : dict) -> Weather:
        '''
        Метод выделяет из JSON-файла с погодой основую информацию и возвращает экземпляр датакласса Weather с этой информацией
        Отдельно обрабатывается часовой пояс, потому что JSON содержит сдвиг от UTC в секундах и его надо привести к типу timezone
        '''
        seconds_shift_from_UTC = int(weather_request_json['timezone'])
        tmzn = timezone(timedelta(seconds=seconds_shift_from_UTC))
        date_and_time = datetime.now(tz = tmzn)

        weather_data = Weather(
            time = date_and_time.strftime("%Y-%d-%m %H:%M:%S %Z"),
            place = weather_request_json['name'],
            weather = weather_request_json['weather'][0]['description'],
            real_temperature = int(weather_request_json['main']['temp']),
            feels_like_temparature = int(weather_request_json['main']['feels_like']),
            wind_speed = weather_request_json['wind']['speed']
        )
        return weather_data
