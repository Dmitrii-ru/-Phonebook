import re
from db_views import db_create, db_read, db_edit
from settings import settings_dict, fields_text, fields_phone


def exit_to_main():
    """
    # Выход в главное меню

    """

    print('_____________________')
    print('Выход в главное меню')
    import main
    main.main()


reg_phone_number = re.compile(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$')


def validate_text(field, field_text_user):
    """
    # Validata введенных данных
    - Проверка полей ['Фамилия', 'Имя', 'Отчество', 'Организация']

    :param field: Имя поля объекта
    :param field_text_user: текст объекта
    :return: True если прошел проверку
    """
    # Получить максимальную длину поля
    max_l = settings_dict.get('max_length_field', 30)
    # Длина введенного текста
    len_obj = len(field_text_user)

    if len_obj < 2:
        print(f'Error:Поле {field} должна содержать не менее 2 символов, введенные данные "{field_text_user}"')
        return False

    elif len_obj > max_l:
        print(f'Error:Поле {field} должна содержать менее 30 символов, '
              f'введенные данные "{field_text_user}" длинна {len(field_text_user)}')
        return False

    elif any(char.isdigit() for char in field_text_user):
        print(f'Error:Поле {field} не должна содержать цифры, введенные данные "{field_text_user}"')
        return False

    return True


def validate_phone_number(field, field_phone_user):
    """
    # Validata введенных данных
    - Проверка полей ['Телефон рабочий', 'Телефон личный']

    :param field: 'Телефон рабочий'
    :param field_phone_user: '+7(929)927-19-00'
    :return: True если прошел проверку
    """

    if not reg_phone_number.match(field_phone_user):  # Поверяем на соответствие регулярному выражению
        print(f'{field_phone_user} должен быть формата +7(XXX)XXX-XX-XX", например: +7(929)927-19-00')
        return False
    return True


def form_create_record():
    """
    # Создаем новую запись в базе данных
    - Предлагаем ввести согласно списку полей для заполнения
    - Если поле не проходит validata, предлагаем ввести данные снова

    """

    new_record = {}
    print('---------------------')
    print("Создание новой записи")
    print('---------------------')
    for field in fields_text:
        while True:
            field_text_user = input(f'{field}: ')
            if field_text_user == 'exit':
                return

            if validate_text(field, field_text_user):  # Если проходим validata
                new_record[field] = field_text_user  # Добавляем новое поле в новую запись
                break

    for field in fields_phone:
        while True:
            field_phone_user = input(f'{field}: ')
            if field_phone_user == 'exit':
               return
            if validate_phone_number(field, field_phone_user):  # Если проходим validata
                new_record[field] = field_phone_user  # Добавляем новое поле в новую запись
                break

    db_create(new_record)  # Создаем новую запись


def form_edit_record():
    """
    # Редактируем поля в таблице
    - Получаем старку, разбиваем на строки объекты, объекты разбиваем на параметры
    - Проверки на корректность введенных данных
    - Передаем данные для изменения
    db_edit(
                {
                    'num_record': num_record,
                    'field': field_user,
                    'new_field_text': new_field_text,
                }
    )
    """
    fields = fields_text + fields_phone
    print('_____________________________________________________________________')
    print('Редактор записей.')
    print('Доступные поля:', ', '.join(fields))
    print('Пример ввода.')
    print('Редактируем одно поле: номер_строки/название_поле/новый_текст.')
    print('Если вы хотение отредактировать несколько полей, разделите их запятой.')
    print('1/Имя/Вася,1/Отчество/Васильевич')
    print('_____________________________________________________________________')

    while True:
        objs = input("Введите данные: ")
        # Количество записей в бахе данных
        len_db = len(db_read())
        if objs == 'exit':
            break

        elif not objs:
            print('Error: Введите данные.')
            continue

        try:
            # Обходим объекты редактирования
            for obj in objs.split(','):
                # Объект редактирования и указания для редакции
                obj_split = obj.split('/')
                # Строка записи
                num_record = int(obj_split[0])
                # Поле которые нужно редактировать
                field_user = obj_split[1]
                # Новое значение
                new_field_text = obj_split[2]

                # Есть ли поле в списке полей программы
                if field_user in fields:
                    # Запускаем проверку введенных данных согласно типу поля
                    if field_user in fields_text:
                        val = validate_text(field_user, new_field_text)
                    else:
                        val = validate_phone_number(field_user, new_field_text)

                    if val:
                        # Проверим корректность номера строки
                        if 1 <= num_record <= len_db:
                            # Запускаем функцию редакции записи
                            db_edit(
                                {
                                    'num_record': num_record,
                                    'field': field_user,
                                    'new_field_text': new_field_text,
                                }
                            )

            break
        except:
            print('Error: Некорректные данные')
            continue


def form_search_record():
    """
    # Функция ищет записи по полям
    - Получаем старку, разбиваем на строки объекты, объекты разбиваем на параметры
    - Проверки на корректность введенных данных
    - Получаем все записи в базе данных, обходим и проверяем на совпадения с входными данными функции
    - Отдаем список найденных записей


    :return: [
        {
          "Фамилия": "Лось",
          "Имя": "Колян",
          "Отчество": "Васильевич",
          "Организация": "Зоопарк",
          "Телефон рабочий": "+7(929)927-19-01",
          "Телефон личный": "+7(929)927-19-01"
        },
        {
          "Фамилия": "Иванов",
          "Имя": "Карл",
          "Отчество": "Васильевич",
          "Организация": "Империя",
          "Телефон рабочий": "+7(929)927-19-02",
          "Телефон личный": "+7(929)927-19-02"
        }
    ]
    """
    fields = fields_text + fields_phone
    print('_____________________________________________________________________')
    print('Поиск записей.')
    print('Доступные поля:', ', '.join(fields))
    print('Пример ввода.')
    print('Ищем по 1 полю: название_поле/текст_поиска.')
    print('Если вы хотение искать по нескольким, разделите их запятой.')
    print('Имя/Вася,Отчество/Васильевич')
    print('_____________________________________________________________________')
    # Словарь параметров поиска
    search_params = {}

    while True:

        objs = input("Введите данные: ")
        db = db_read()
        if objs == 'exit':
            exit_to_main()

        elif not db:
            print('Error: Справочник пуст.')
            break

        elif not objs:
            print('Error: Введите данные.')
            continue

        try:
            # Обходим объекты поиска
            for obj in objs.split(','):
                # Поле поиска и значение
                obj_s = obj.split('/')

                search_field = obj_s[0]
                search_text = obj_s[1]

                # Проверка корректности введенного поля
                if search_field in fields:
                    # Добавляем или заменяем параметры поиска
                    search_params.setdefault(search_field, search_text)

            if search_params:
                data = []
                # Обходим базу данных
                for record in db:
                    # Обходим search_params и вхождение текста поиска в поле поиска
                    if all(v.lower() in record[k].lower() for k, v in search_params.items()):
                        data.append(record)
                return data
            break

        except:
            print('Error: Некорректные данные')
            continue
