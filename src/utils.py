import psycopg2
import requests


def get_data(data: list) -> list:
    """
    Take a list of companies ID from hh.ru and return a list of dicts
    :param data: list of companies ID
    :return: list of dicts
    """
    result = []
    for item in data:
        url = f'https://api.hh.ru/employers/{item}'
        response_employer = requests.get(url).json()
        response_vacancies = requests.get(response_employer['vacancies_url']).json()
        result.append({'employer': response_employer,
                       'vacancies': response_vacancies['items']})

    return result


def create_db(name: str, params: dict) -> None:
    """
    Create database in postgres
    :param name: name of the future database
    :param params: params to connection
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    curs = conn.cursor()

    curs.execute(f'DROP DATABASE IF EXISTS {name}')
    curs.execute(f'CREATE DATABASE {name}')

    conn.close()


def create_tables(name: str, params: dict) -> None:
    """
    Создает таблицы в базе данных
    :param name: имя базы данных
    :param params: параметры для подключения
    """
    conn = psycopg2.connect(database=name, **params)

    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("""CREATE TABLE IF NOT EXISTS companies
                                (
                                    company_id SERIAL PRIMARY KEY,
                                    company_name VARCHAR(100) NOT NULL,
                                    link VARCHAR(250) NOT NULL
                                );""")
                curs.execute("""CREATE TABLE IF NOT EXISTS vacancies
                                (
                                    vacancy_id SERIAL PRIMARY KEY,
                                    company_id INT NOT NULL,
                                    FOREIGN KEY(company_id) REFERENCES companies(company_id),
                                    title_vacancy VARCHAR(150) NOT NULL,
                                    salary INT,
                                    link VARCHAR(250) NOT NULL,
                                    description TEXT
                                );""")
    finally:
        conn.close()


def salary_format(value):
    if value is not None:
        if value['from'] is not None and value['to'] is not None:
            return round((value['from'] + value['to']) / 2)
        elif value['from'] is not None:
            return value['from']
        elif value['to'] is not None:
            return value['to']


def filling_database(data: list, name: str, params: dict) -> None:
    """
    Заполнение таблиц данными
    :param data: список таблиц
    :param name: имя базы данных
    :param params: параметры для подключения
    """
    conn = psycopg2.connect(database=name, **params)

    try:
        with conn:
            with conn.cursor() as curs:
                for item in data:
                    curs.execute('INSERT INTO companies (company_name, link)'
                                 'VALUES (%s, %s)'
                                 'returning company_id',
                                 (item['employer'].get("name"),
                                  item['employer'].get("alternate_url")))

                    company_id = curs.fetchone()[0]

                    for part in item['vacancies']:
                        salary = salary_format(part["salary"])
                        curs.execute('INSERT INTO vacancies'
                                     '(company_id, title_vacancy, salary, link, description)'
                                     'VALUES (%s, %s, %s, %s, %s)',
                                     (company_id,
                                      part["name"],
                                      salary,
                                      part["alternate_url"],
                                      part["snippet"].get("responsibility")))
    finally:
        conn.close()
