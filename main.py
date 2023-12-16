from src.class_db_manager import DBManager
from src.config import config
from src.utils import create_db, create_tables, filling_database, get_data

if __name__ == '__main__':
    employers_list = []
    introductory = 10

    print('Введите идентификаторы работодателей или "0" (ноль) для прерывания работы\n')

    while introductory > 0:
        us_input = int(input())
        introductory -= 1
        if us_input != 0:
            employers_list.append(us_input)
        else:
            break

    print(employers_list)

    script_file = 'create_db.sql'
    db_name = input('Введите название Вашей базы данных: ')
    params = config()

    create_db(db_name, params)
    print(f'База данных {db_name} успешно создана.')

    # params.update({'dbname': db_name})

    create_tables(db_name, params)
    filling_database(get_data(employers_list), db_name, params)

    db_manager = DBManager(db_name, params)
    while True:
        print('-' * 50)
        print('Главное меню:\n')
        print('Введите "1", чтобы получить данные обо всех компаниях и вакансиях\n')
        print('Введите "2", чтобы получить все вакансии\n')
        print('Введите "3", чтобы получить среднюю зарплату для вакансий\n')
        print('Введите "4", чтобы получить вакансии с более высокой зарплатой\n')
        print('Введите "5", чтобы получить вакансии с ключевым словом\n')
        print('Введите "0", чтобы выйти\n')

        user_input = input('Выберите действие ')
        match user_input:
            case '1':
                print('-' * 50)
                print(db_manager.get_companies_and_vacancies_count())
            case '2':
                print('-' * 50)
                print(db_manager.get_all_vacancies())
            case '3':
                print('-' * 50)
                print(db_manager.get_avg_salary())
            case '4':
                print('-' * 50)
                print(db_manager.get_vacancies_with_higher_salary())
            case '5':
                print('-' * 50)
                keyword = input('Введите ключевое слово: ').lower()
                print(db_manager.get_vacancies_with_keyword(keyword))
            case '0':
                print('-' * 50)
                print('-' * 50)
                quit('Программа была деактивирована')
            case _:
                print('-' * 50)
                print('Неизвестное действие')
