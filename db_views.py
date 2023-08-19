import json


def move_bad_data_to_file(source_file):
    with open(source_file, 'r', encoding='utf-8') as file:
        content = file.read()
    with open('bad_data.txt', 'w', encoding='utf-8') as bad_file:
        bad_file.write(content)


def db_manager(method=None, obj=None):
    """
    Создаем запись или отдаем все записи
    Validate на нужный формат файла

    :param method: 'r' or 'w'
    :param obj: 'new record'
    :return: if method=='r' get all records
    """

    try:
        if method == 'r':
            with open('phonebook.txt', 'r') as file:
                data = json.load(file)  # encode в json
                return data
        elif method == 'w':
            existing_data = db_manager(method='r', obj=obj)  # Загрузить существующие данные
            if existing_data is None:  # Смотрим пустая ли бд
                existing_data = []  # Добавляем список
            existing_data.append(obj)  # Добавить новый словарь
            with open('phonebook.txt', 'w') as file:
                json.dump(existing_data, file)  # encode в json, добавляем в бд

    except (FileNotFoundError, json.JSONDecodeError):  # Если не получилось decoded json
        print('База данных отсутствует или была повреждена, создаем новую')
        with open('phonebook.txt', 'w', encoding='utf-8') as clean_file:  # Open or create and open
            move_bad_data_to_file('phonebook.txt')  # Переносим поврежденный данные в спец. файл
            clean_file.truncate(0)  # Очистить phonebook.txt
            json.dump([], clean_file)  # Создаем пустой список


def db_read():
    return db_manager(method='r')  # Получаем decoded список записей


def db_create(new_record):
    db_manager(method='w', obj=new_record)


# Функция для вывода записей из справочника
# def display_records():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as file:
#
#             print(*
#                   [
#                       centered_string('Фамилия'),
#                       centered_string('Имя'),
#                       centered_string('Отчество'),
#                       centered_string('Организация'),
#                       centered_string('Телефон рабочий'),
#                       centered_string('Телефон личный'),
#                   ]
#                   )
#             for line in file:
#                 parts = line.strip().split(',')
#                 print(*parts)
#     else:
#         print("Справочник пуст")
