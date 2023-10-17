from weather_client import WeatherClient
from custom_exceptions import *
from lines_for_user import *
import requests
from weather_dataclass import CurrentWeather

def main():
    print(GREETING_LINE + INFO_LINE)
    client = WeatherClient()

    while True:
        user_input = input(INVITING_LINE)
        match user_input:
            case "Показать историю":
                history = client.get_history()
                number_of_history_items = input(NUMBER_OF_HISTORY_LINE)
                try:
                    number = min(int(number_of_history_items), len(history))
                except:
                    print(WRONG_INPUT_LINE)
                    continue
                for data in history[-number:]:
                    weather = prepare_history(data)
                    print(generate_report(weather))
                continue
            case "Очистить историю":
                client.clear_history()
                print('История очищена')
            case "Справка":
                print(INFO_LINE)
            case "Выйти":
                break
            case _:
                print_response(client, user_input)


def print_response(client : WeatherClient, user_input : str):
    try:
        response = client.get_weather(user_input)
    except InvalidInputException:
        print(WRONG_INPUT_LINE)
    except EmptyInputException:
        print(EMPTY_INPUT_LINE)
    except LocationException:
        print(UNKNOWN_GEOLOCATION_LINE)
    except APIRequestException:
        print(FAILED_API_REQUEST_LINE)
    except requests.exceptions.ConnectionError:
        print(NO_CONNECTION_LINE)
    except requests.exceptions.JSONDecodeError:
        print(UNKNOWN_ERROR_LINE)
    except Exception:
        print(UNKNOWN_ERROR_LINE)
    else:
        report_for_user = generate_report(response)
        print(report_for_user)
        client.log_to_history(response)

def generate_report(weather_info : CurrentWeather) -> str:
    report = f"Текущее время: {weather_info.time}\n" \
            f"Название города: {weather_info.place}\n" \
            f"Погодные условия: {weather_info.weather}\n" \
            f"Текущая температура: {weather_info.real_temperature} градусов по цельсию\n" \
            f"Ощущается как: {weather_info.feels_like_temparature} градусов по цельсию\n" \
            f"Скорость ветра: {weather_info.wind_speed} м/c"
    return report

def prepare_history(weather_data : dict) -> CurrentWeather:
    weather = CurrentWeather(
        weather_data['time'],
        weather_data['place'],
        weather_data['weather'],
        weather_data['real_temperature'],
        weather_data['feels_like_temparature'],
        weather_data['wind_speed']
    )
    return weather

if __name__ == "__main__":
    main()