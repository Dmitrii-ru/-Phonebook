import os
import re
from db_views import db_create
from settings import settings_dict

reg_phone_number = re.compile(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$')


def centered_string(obj):
    variable = obj
    total_width = settings_dict['max_length_field']
    padding = (total_width - len(variable)) // 2
    obj = ' ' * padding + variable + ' ' * padding
    if len(obj) < total_width:
        obj = obj + ' '
    return '|' + obj + '|'


def validate_text(name):
    """
    Просим пользователи вводить данные пока они не будут отвечать требованием

    :param name: Название текущего параметра
    :return: Validate data
    """

    while True:
        max_l = settings_dict['max_length_field']
        obj = input(f'{name}: ')
        len_obj = len(obj)
        if len_obj < 2:
            print(f'{name} должна содержать не менее 2 символов')
            continue
        if len_obj > max_l:
            print(f'{name} должна содержать менее 30 символов, сейчас {len_obj}')
            continue

        if any(char.isdigit() for char in obj):
            print(f'{name} не должна содержать цифры')
            continue

        return obj


def validate_phone_number(name):
    """
    Просим пользователи вводить данные пока они не будут отвечать требованием

    :param name: Название текущего параметра
    :return: Validate data
    """

    while True:
        obj = input(f'{name}: ')

        if not reg_phone_number.match(obj):  # Поверяем на соответствие регулярному выражению
            print(f'{name} должен быть формата +7(XXX)XXX-XX-XX", например: +7(929)927-19-00')
            continue

        return obj


def form_new_record():
    last_name = validate_text('Фамилия')
    first_name = validate_text('Имя')
    middle_name = validate_text('Отчество')
    organization = validate_text('Организация')
    work_phone = validate_phone_number('Телефон рабочий')
    personal_phone = validate_phone_number('Телефон личный')

    new_record = {
        "Фамилия": last_name,
        "Имя": first_name,
        "Отчество": middle_name,
        "Организация": organization,
        "Телефон рабочий": work_phone,
        "Телефон личный": personal_phone,
    }

    db_create(new_record)


