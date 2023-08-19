from forms import form_new_record
from db_views import db_read
from settings import settings_dict


def centered_string(obj):
    variable = obj
    total_width = settings_dict['max_length_field']
    padding = (total_width - len(variable)) // 2
    obj = ' ' * padding + variable + ' ' * padding
    if len(obj) < total_width:
        obj = obj + ' '
    return '|' + obj + '|'


def display_menu():
    print('______________________')
    print("Телефонный справочник.")
    print("1. Вывод записей")
    print("2. Добавление записи")
    print("3. Редактирование записи")
    print("4. Поиск записей")
    print("5. Выход")
    print('_______________________')


def display_records():
    data = db_read()

    if not data:
        print('В телефонном справочнике нет записей')
    else:
        print(*
              [
                  centered_string('№'),
                  centered_string('Фамилия'),
                  centered_string('Имя'),
                  centered_string('Отчество'),
                  centered_string('Организация'),
                  centered_string('Телефон рабочий'),
                  centered_string('Телефон личный'),
              ]
              )
        for idx, record in enumerate(data, start=1):  # Обходим список, проставляем номер строк
            print(*
                  [
                      centered_string(str(idx)),
                      centered_string(record['Фамилия']),
                      centered_string(record['Имя']),
                      centered_string(record['Отчество']),
                      centered_string(record['Организация']),
                      centered_string(record['Телефон рабочий']),
                      centered_string(record['Телефон личный']),
                  ]
                  )

            # values = list(entry.values())  # Получаем список значений
            # print(f"{idx}. {', '.join(values)}")


def edit_record():
    pass


def search_records():
    pass


def main():
    while True:
        display_menu()
        choice = input("Выберите действие: ")
        if choice == "1":
            display_records()
        elif choice == "2":
            form_new_record()
        elif choice == "3":
            edit_record()
        elif choice == "4":
            search_records()
        elif choice == "5":
            break
        else:
            print("Некорректный выбор")


if __name__ == "__main__":
    main()
