from strenum import StrEnum
from weather_client import WeatherClient
from custom_exceptions import *
from lines_for_user import *
import requests
from weather_dataclass import Weather

class Commands(StrEnum):
    SHOW_HISTORY = '-sh'
    CLEAR_HISTORY = '-ch'
    SHOW_INFO = '-i'
    EXIT = '-e'

def main():
    print(GREETING_LINE + INFO_LINE)
    client = WeatherClient()

    while True:
        try:
            user_input = input(INVITING_LINE).strip().lower()
            match user_input:
                case Commands.SHOW_HISTORY:
                    print(prepare_history(client))
                case Commands.CLEAR_HISTORY:
                    client.clear_history()
                    print(HISTORY_CLEARED_LINE)
                case Commands.SHOW_INFO:
                    print(INFO_LINE)
                case Commands.EXIT:
                    break
                case _:
                    print_response(client, user_input)
        except Exception:
            print(UNKNOWN_ERROR_LINE)
            continue


def print_response(client : WeatherClient, user_input : str) -> None:
    '''
    Функция формирует ответ на запрос пользователя
    В случае удачного запроса производится вывод данных о погоде и запись ее в историю
    В случае неудачного запроса выводится информационное сообщение на основе данных о причине неудачи
    '''
    try:
        response = client.get_weather(user_input)
    except CUSTOM_EXCEPTIONS as e:
        print(e.message)
    except requests.exceptions.ConnectionError:
        print(NO_CONNECTION_LINE)
    except requests.exceptions.JSONDecodeError:
        print(FAILED_API_REQUEST_LINE)
    else:
        report_for_user = str(response)
        print(report_for_user)
        client.log_to_history(response)


def prepare_history(client : WeatherClient) -> str:
    '''
    Функция ответственна за вывод истории запросов
    После вызова функция получает от клиента историю запросов в формате list[dict]
    и создает на ее основе печатный текст истории для пользователя
    В случае, если история пуста, выводится соответствующее сообщение
    '''
    try:
        history_list = client.get_history()
        number_of_history_items = input(NUMBER_OF_HISTORY_LINE).strip()
        number = min(int(number_of_history_items), len(history_list))
    except Exception:
        print(UNABLE_TO_GET_HISTORY_LINE)

    history_str = ''
    for data in history_list[number::-1]:
        weather = Weather(**data)
        history_str += str(weather) + '\n'
    
    if len(history_str) == 0:
        return EMPTY_HISTORY_LINE
    else:
        return history_str


if __name__ == "__main__":
    main()