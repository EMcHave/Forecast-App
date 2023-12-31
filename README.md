# Основные сведения
1. Работа с запросами обернута в класс WeatherClient
    - Публичные методы:
        - get_weather() - возвращает данные о погоде по запросу
        - log_to_history() - осуществляет запись истории
        - get_history() - возвращает записанную историю, если она существует
        - clear_history() - очищает историю
    - Приватные методы имеют наименования, начинающиеся на __ и содержат вспомогательные действия при запросах погоды и работы с файлами
1. HTTP-запросы реализованы через библиотеку **_requests_**, установка других пакетов не требуется
1. Для запуска программы необходимо клонировать репозиторий и запустить файл **_main.py_**
1. Основные команды выводятся пользователю при запуске или по запросу "-i"
1. Программа задействует следующие вспомогательные модули:
    - storage.py - содержит класс Storage для работы с чтением/записью JSON-файлов
    - custom_exceptions.py - заглушки исключений для разных сценариев поведения
    - lines_for_user.py - набор константных строк для общения с пользователем
    - weather_dataclass.py - датакласс для передачи обработанного запроса погоды
# Пример работы программы
```
PS C:\Users\mchav\source\Python HW\Forecast App\app> python main.py
Здравствуйте! Данный сервис предоставляет данные о погоде в любой точке мира
Вам доступен следюущий функционал:
— Для получения сведений о погоде в населенном введите его название
— Для получения сведений о погоде по вашему местоположению введите "Мое местоположение"
— Для вывода истории запросов введите "Показать историю"
— Для очистки истории запросов введите "Очистить историю"
— Для выхода введите "Выйти"
— Для получения справки введите "Справка"
Введите ваш запрос
Москва
Текущее время: 2023-17-10 13:56:35 UTC+03:00
Название города: Москва
Погодные условия: пасмурно
Текущая температура: 3 градусов по цельсию
Ощущается как: 0 градусов по цельсию
Скорость ветра: 6.59 м/c
Введите ваш запрос
Газа
Текущее время: 2023-17-10 13:56:37 UTC+03:00
Название города: Газа
Погодные условия: ясно
Текущая температура: 25 градусов по цельсию
Ощущается как: 26 градусов по цельсию
Скорость ветра: 4.56 м/c
Введите ваш запрос
Очистить историю
История очищена
Введите ваш запрос
Выйти
PS C:\Users\mchav\source\Python HW\Forecast App\app>
```