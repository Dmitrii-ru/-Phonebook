import json


def db_manager(method=None, obj=None, ):
    path = 'database/phonebook.txt'

    """
    Функция работы с базой данных

    """
    if method == 'GET':
        """
        Возвращаем все данные бд

        """

        try:
            with open(path, 'r') as file:
                data = json.load(file)  # encode в json
                return data
        except (FileNotFoundError, json.JSONDecodeError):  # Если не получилось decoded json
            print('ERROR :База данных отсутствует или была повреждена, создаем новую')
            with open(path, 'w', encoding='utf-8') as clean_file:  # Open or create and open
                clean_file.truncate(0)  # Очистить phonebook.txt
                data = json.dump([], clean_file)  # Создаем пустой список
                return data

    elif method == 'POST':

        """
        Запись новых данных в базу данных
        
        """

        existing_data = db_manager(method='GET')  # Загрузить существующие данные
        if existing_data is None:  # Смотрим пустая ли бд
            existing_data = []  # Приводим файл в формат list
        else:
            if obj in existing_data:
                return print('Такая запись уже есть')
        existing_data.append(obj)  # Добавить новый словарь
        try:

            with open(path, 'w') as file:
                json.dump(existing_data, file, indent=2, ensure_ascii=False)  # Записываем новые данные
            print("Запись успешно добавлена.")
        except OSError as e:
            return print(f"ERROR : Ошибка записи в базу данных: {e}")

    elif method == 'PUT':
        """
        Обновляю поля записей 
        
        """

        existing_data = db_manager(method='get')  # Загрузить существующие данные
        index_obj = obj['num_record'] - 1  # Индекс
        field = obj['field']  # Поле которое нужно изменить
        new_field_text = obj['new_field_text']  # На что нужно изменить
        existing_data[index_obj][field] = new_field_text  # Меняем значение

        try:
            with open(path, 'w') as file:
                json.dump(existing_data, file, indent=2, ensure_ascii=False)  # Обновляем данные
            print("Записи успешно обновлены.")
        except OSError as e:
            return print(f"ERROR : Ошибка записи в базу данных: {e}")


def db_read():
    return db_manager(method='GET')  # Получить decoded список записей


def db_create(new_record, custom_path=None):
    db_manager(method='POST', obj=new_record)  # Создать новую запись


def db_edit(edit_record):
    db_manager(method='PUT', obj=edit_record)  # Изменить запись
