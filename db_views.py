import json


def move_bad_data_to_file(source_file):
    with open(f'database/{source_file}', 'r', encoding='utf-8') as file:
        content = file.read()
    with open('database/bad_data.txt', 'w', encoding='utf-8') as bad_file:
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
            with open('database/phonebook.txt', 'r') as file:
                data = json.load(file)  # encode в json
                return data
        elif method == 'w':
            existing_data = db_manager(method='r', obj=obj)  # Загрузить существующие данные
            if obj in existing_data:
                return print('Такая запись уже есть ')

            if existing_data is None:  # Смотрим пустая ли бд
                existing_data = []  # Приводим файл в формат list
            existing_data.append(obj)  # Добавить новый словарь

            try:
                with open('database/phonebook.txt', 'w') as file:
                    json.dump(existing_data, file, indent=2, ensure_ascii=False)  # Загрузить существующие данные
                print("Запись успешно добавлена.")
            except OSError as e:  # Обработка в случаи не возможности записи
                print(f"ERROR : Ошибка записи в файл: {e}")


    except (FileNotFoundError, json.JSONDecodeError):  # Если не получилось decoded json
        print('ERROR :База данных отсутствует или была повреждена, создаем новую')
        with open('database/phonebook.txt', 'w', encoding='utf-8') as clean_file:  # Open or create and open
            move_bad_data_to_file('phonebook.txt')  # Переносим поврежденный данные в спец. файл
            clean_file.truncate(0)  # Очистить phonebook.txt
            json.dump([], clean_file)  # Создаем пустой список


def db_read():
    return db_manager(method='r')  # Получаем decoded список записей


def db_create(new_record):
    db_manager(method='w', obj=new_record)  # Создаем новую запись

