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

    :param field: 'Имя'
    :param field_text_user: 'Толя'
    :return: True если прошел проверку
    """

    max_l = settings_dict.get('max_length_field', 30)
    len_obj = len(field_text_user)
    obj = field_text_user
    if len_obj < 2:
        print(f'Error:Поле {field} должна содержать не менее 2 символов, введенные данные "{field_text_user}"')
        return False

    elif len_obj > max_l:
        print(f'Error:Поле {field} должна содержать менее 30 символов, '
              f'введенные данные "{field_text_user}" длинна {len(field_text_user)}')
        return False

    elif any(char.isdigit() for char in obj):
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
    obj = field_phone_user
    if obj == 'exit':
        exit_to_main()
    elif not reg_phone_number.match(obj):  # Поверяем на соответствие регулярному выражению
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

    for field in fields_text:
        while True:
            field_text_user = input(f'{field}: ')
            if field_text_user == 'exit':
                exit_to_main()
            if validate_text(field, field_text_user):
                new_record[field] = field_text_user
                break

    for field in fields_phone:
        while True:
            field_phone_user = input(f'{field}: ')
            if field_phone_user == 'exit':
                exit_to_main()
            if validate_phone_number(field, field_phone_user):
                new_record[field] = field_phone_user
                break
    db_create(new_record)


def form_edit_record():
    """
    # Редактируем поля в таблице
    - Получаем старку, разбиваем на строки объекты, объекты разбиваем на параметры
    - Проверки на корректность введенных данных
    - Передаем данные для изменения

    """
    params = fields_text + fields_phone
    print('_____________________________________________________________________')
    print('Редактор записей.')
    print('Доступные поля:', ', '.join(params))
    print('Пример ввода.')
    print('Редактируем одно поле: номер_строки/название_поле/новый_текст.')
    print('Если вы хотение отредактировать несколько полей, разделите их запятой.')
    print('1/Имя/Вася,1/Отчество/Васильевич')
    print('_____________________________________________________________________')

    while True:

        objs = input("Введите данные: ")
        len_db = len(db_read())
        if objs == 'exit':
            break

        elif not objs:
            print('Error: Введите данные.')
            continue

        try:
            for obj in objs.split(','):
                obj_s = obj.split('/')

                num_record = int(obj_s[0])
                field = obj_s[1]
                new_field_text = obj_s[2]

                if field in params:
                    if field in fields_text:
                        val = validate_text(field, new_field_text)
                    else:
                        val = validate_phone_number(field, new_field_text)

                    if val:
                        if 1 <= num_record <= len_db:
                            db_edit(
                                {
                                    'num_record': num_record,
                                    'field': field,
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
    params = fields_text + fields_phone
    print('_____________________________________________________________________')
    print('Поиск записей.')
    print('Доступные поля:', ', '.join(params))
    print('Пример ввода.')
    print('Ищем по 1 полю: название_поле/текст_поиска.')
    print('Если вы хотение искать по нескольким, разделите их запятой.')
    print('Имя/Вася,Отчество/Васильевич')
    print('_____________________________________________________________________')
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

            for obj in objs.split(','):
                obj_s = obj.split('/')

                search_field = obj_s[0]
                search_text = obj_s[1]

                if search_field in params:
                    search_params.setdefault(search_field, search_text)

            if search_params:
                data = []
                for record in db:
                    if all(v.lower() in record[k].lower() for k, v in search_params.items()):
                        data.append(record)
                return data
            break

        except:
            print('Error: Некорректные данные')
            continue
