import json

def db_manager(method=None, obj=None):

    if method == 'get':
        try:
            if method == 'get':
                with open('database/phonebook.txt', 'r') as file:
                    data = json.load(file)  # encode в json
                    return data
        except (FileNotFoundError, json.JSONDecodeError):  # Если не получилось decoded json
            print('ERROR :База данных отсутствует или была повреждена, создаем новую')
            with open('database/phonebook.txt', 'w', encoding='utf-8') as clean_file:  # Open or create and open
                clean_file.truncate(0)  # Очистить phonebook.txt
                data = json.dump([], clean_file)  # Создаем пустой список
                return data

    elif method == 'post':
        existing_data = db_manager(method='get')  # Загрузить существующие данные
        if obj in existing_data:
            return print('Такая запись уже есть')
        if existing_data is None:  # Смотрим пустая ли бд
            existing_data = []  # Приводим файл в формат list
        existing_data.append(obj)  # Добавить новый словарь
        try:
            with open('database/phonebook.txt', 'w') as file:
                json.dump(existing_data, file, indent=2, ensure_ascii=False)  # Записываем новые данные
            print("Запись успешно добавлена.")
        except OSError as e:  # Обработка в случаи не возможности записи
            return print(f"ERROR : Ошибка записи в базу данных: {e}")

    elif method == 'put':
        existing_data = db_manager(method='get')
        index_obj = obj['num_record'] - 1
        field = obj['field']
        new_field_text = obj['new_field_text']
        existing_data[index_obj][field] = new_field_text

        try:
            with open('database/phonebook.txt', 'w') as file:
                json.dump(existing_data, file, indent=2, ensure_ascii=False)  # Записываем новые данные
            print("Запись успешно обновлены.")
        except OSError as e:  # Обработка в случаи не возможности записи
            return print(f"ERROR : Ошибка записи в базу данных: {e}")


def db_read():
    return db_manager(method='get')  # Получаем decoded список записей


def db_create(new_record):
    db_manager(method='post', obj=new_record)  # Создаем новую запись


def db_edit(edit_record):
    db_manager(method='put', obj=edit_record)  # Изменяем запись
