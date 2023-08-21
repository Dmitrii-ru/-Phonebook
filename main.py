from forms import form_create_record, form_edit_record, form_search_record
from db_views import db_read
from settings import settings_dict, fields_text, fields_phone


def centered_string(obj, custom_wight=None):
    """
    # Функция центрует запись при отображении таблицы
    :param obj: текст центровки
    :param custom_wight: кастамные настройки ширины ячейки
    :return: строка с текстом по центру ячейки
    """

    try:
        variable = obj
        total_width = settings_dict['max_length_field']
        if custom_wight:
            total_width = custom_wight

        padding = (total_width - len(variable)) // 2
        obj = ' ' * padding + variable + ' ' * padding
        if len(obj) < total_width:
            obj = obj + ' '
        return obj

    except:
        print(f'Не корректные данные: {obj}')
        return main()


def display_menu():
    print('______________________')
    print("Телефонный справочник.")
    print("1. Вывод записей")
    print("2. Добавление записи")
    print("3. Редактирование записи")
    print("4. Поиск записей")
    print("5. Выход")
    print('_______________________')


def display_records(search=False):
    """
    # Функция выводит справочник в консоль
    :param search:True маркер который говорит о том что нужно сделать поиск по полям

    """
    fields = fields_text + fields_phone

    if search:
        """
        ## search == True
        - Запускает функцию поиска записи по введенным данным 
        - Отображение отфильтрованных данных 
        - Вывод шапки таблицы и данных
        """

        data = form_search_record()
        if not data:
            print('Не чего не найдено')
            main()

        str_fields = '|'.join(centered_string(s) for s in fields)
        header = f'Результаты поиска: найдено {len(data)}.'
        print(centered_string(header, len(str_fields)))
        print("=" * len(str_fields))
        print(str_fields)
        print("-" * len(str_fields))
        for record in data:
            record_strings = [centered_string(record[field]) for field in fields]
            print('|'.join(record_strings))

    else:
        """
        ## search == False
        - Получаем содержимое базы данных
        - Вывод шапки таблицы и данных
        """

        data = db_read()
        if not data:
            print('Ваш справочник пуст')
            main()

        str_fields = '|'.join(centered_string(s) for s in ['№'] + fields)
        header = "Ваш справочник:"
        print(centered_string(header, len(str_fields)))
        print("=" * len(str_fields))
        print(str_fields)
        print("-" * len(str_fields))
        num_record = 1

        for record in data:
            record_strings = [centered_string(record[field]) for field in fields]
            print('|'.join([centered_string(str(num_record))] + record_strings))
            num_record += 1


def main():
    """
    # Главное меню

    """
    while True:
        display_menu()
        choice = input("Выберите действие: ")
        if choice == "1":
            display_records()
        elif choice == "2":
            form_create_record()
        elif choice == "3":
            form_edit_record()
        elif choice == "4":
            display_records(search=True)
        elif choice == "5":
            break
        else:
            print("Некорректный выбор")


if __name__ == "__main__":
    main()
