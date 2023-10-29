import os
import json
class Storage:
    '''
    Класс для работы с файлами в заданной директории
    В конструктор принимает адрес директории
    Реализует чтение JSON-файлов, запись в них и очистку 
    '''

    
    def __init__(self, working_directory : str) -> None:
        self.working_directory = working_directory


    def log_to_json(self, file_name : str, new_dict : dict) -> None:
        '''
        Осуществляет запись в указанный аргументом JSON-файл, находящийся в рабочей директории класса
        '''
        path_to_file = os.path.join(self.working_directory, file_name)
        if not self.__file_exists(file_name) or self.__is_file_empty(file_name):
            with open(path_to_file, 'a+') as file:
                history_objects = []
                history_objects.append(new_dict)
                json.dump(history_objects, file, indent=3, default=str)
        else:
            with open(path_to_file, 'r+') as file:
                history_objects = json.load(file)
                history_objects.append(new_dict)
                file.seek(0)
                json.dump(history_objects, file, indent=3, default=str)
       

    def read_from_json(self, file_name : str) -> list[dict]:
        '''
        Читает из файла историю класса, возвращая список словарей с данными о погоде
        '''
        path_to_file = os.path.join(self.working_directory, file_name)
        if self.__file_exists(file_name) and not self.__is_file_empty(file_name):
            with open(path_to_file, 'r') as file:
                return json.load(file)
        else:
            return []
        
        
    def clear_file(self, file_name : str) -> None:
        '''
        Очищает файл, указанный в аргументе
        '''
        path_to_file = os.path.join(self.working_directory, file_name)
        with open(path_to_file, 'w') as file:
            pass


    def __file_exists(self, file_name : str) -> bool:
        '''Проверяет есть ли указанный файл в рабочей директории класса'''
        return os.path.isfile(
            os.path.join(self.working_directory, file_name)
        )
    

    def __is_file_empty(self, file_name : str) -> bool:
        '''Проверяет пуст ли указанный файл в рабочей директории класса'''
        return os.path.getsize(
            os.path.join(self.working_directory, file_name)
        ) == 0
    