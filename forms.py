import re
from db_views import db_create, db_read, db_edit
from settings import settings_dict, fields_text, fields_phone


def exit_to_main():
    print('_____________________')
    print('Выход в главное меню')
    import main
    main.main()


reg_phone_number = re.compile(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$')


def validate_text(param, param_user):
    max_l = 30
    len_obj = len(param_user)
    obj = param_user
    if len_obj < 2:
        print(f'Error:Поле {param} должна содержать не менее 2 символов, введенные данные "{param_user}"')
        return False

    elif len_obj > max_l:
        print(f'Error:Поле {param} должна содержать менее 30 символов, '
              f'введенные данные "{param_user}" длинна {len(param_user)}')
        return False

    elif any(char.isdigit() for char in obj):
        print(f'Error:Поле {param} не должна содержать цифры, введенные данные "{param_user}"')
        return False

    return True


def validate_phone_number(param, param_user):
    obj = param_user
    if obj == 'exit':
        exit_to_main()
    elif not reg_phone_number.match(obj):  # Поверяем на соответствие регулярному выражению
        print(f'{param_user} должен быть формата +7(XXX)XXX-XX-XX", например: +7(929)927-19-00')
        return False
    return True


def form_create_record():
    new_record = {}

    for param in fields_text:
        while True:
            param_user = input(f'{param}: ')
            if param_user == 'exit':
                exit_to_main()
            if validate_text(param, param_user):
                new_record[param] = param_user
                break

    for param in fields_phone:
        while True:
            param_user = input(f'{param}: ')
            if param_user == 'exit':
                exit_to_main()
            if validate_phone_number(param, param_user):
                new_record[param] = param_user
                break
    db_create(new_record)


def form_edit_record():
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
                        if num_record <= len_db:
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
