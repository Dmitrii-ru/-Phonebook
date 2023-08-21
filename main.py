from database.generator_db import generate_records
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
        # Если нет custom_wight то берем settings_dict['max_length_field']
        total_width = custom_wight if custom_wight else settings_dict['max_length_field']
        # Вычислим отступы
        padding = (total_width - len(variable)) // 2
        # Центруем obj в ячейке
        obj = ' ' * padding + variable + ' ' * padding
        # Проверяем погрешность при // 2
        if len(obj) < total_width:
            obj = obj + ' '
        return obj

    except:
        print(f'Не корректные данные: {obj}')
        return main()


def display_records(search=False):
    """
    # Функция выводит справочника в консоль
    :param search:True маркер который говорит о том что нужно сделать поиск по полям

    """
    # Объединяем default поля в 1 список
    fields = fields_text + fields_phone

    if search:
        """
        ## search == True
        - Запускает функцию поиска записи по введенным данным 
        - Отображение отфильтрованных данных 

        """
        # Запускаем функцию приема данных для поиска
        data = form_search_record()
        if not data:
            print('Не чего не найдено')
            main()
        # Формируем список полей для header
        str_fields = '|'.join(centered_string(s) for s in fields)
        # Формируем header
        header = f'Количество совпадений по запросу: {len(data)}.'
        # Длинна списка полей
        custom_wight = len(str_fields)
        # Задаем длину таблицы
        print(centered_string(header, custom_wight))
        print("=" * custom_wight)
        print(str_fields)
        print("-" * custom_wight)
        # Обходим все записи
        for record in data:
            # Формируем строку, обходим default поля, берем нужные поля из record и центруем в ячейке
            record_strings = [centered_string(record[field]) for field in fields]
            print('|'.join(record_strings))

    else:
        """
        ## search == False
        - Получаем содержимое базы данных
        - Отображение данных 
        """
        # Получаем данные из базы данных
        data = db_read()
        if not data:
            print('Ваш справочник пуст')
            main()
        # Все то же самое что и в search кроме нумерации строк
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
    Главное меню программы.

    В цикле отображается главное меню с вариантами действий.
    Пользователь выбирает действие, вводя соответствующую цифру.

    """

    while True:
        print('______________________')
        print("Телефонный справочник.")
        print("1. Список контактов")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск записей")
        print("5. Создать 100 записей в базу данных")
        print("6. Выход")
        print('_______________________')

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
            generate_records()
        elif choice == "6":
            break
        else:
            print("Некорректный выбор")


if __name__ == "__main__":
    main()
