import psycopg2


class DBManager:

    def __init__(self, db_name: str, params: dict):
        self.database_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> list[tuple] or str:
        """
        Получает список всех компаний и количество вакансий для каждой из них.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as curs:
                curs.execute('SELECT company_name, COUNT(vacancy_id) '
                             'FROM companies '
                             'JOIN vacancies USING (company_id) '
                             'GROUP BY company_name '
                             'ORDER BY company_name')
                result = curs.fetchall()

        except (Exception, psycopg2.DatabaseError) as err:
            return err

        conn.close()
        return result

    def get_all_vacancies(self) -> list[tuple] or str:
        """
        Получает список всех вакансий с указанием названия компании,
        название вакансии, размер зарплаты и ссылку на вакансию.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as curs:
                curs.execute('SELECT title_vacancy, company_name, salary, vacancies.link '
                             'FROM vacancies '
                             'JOIN companies USING (company_id);')

                result = curs.fetchall()

        except (Exception, psycopg2.DatabaseError) as err:
            return err

        conn.close()
        return result

    def get_avg_salary(self) -> list[tuple] or str:
        """
        Получает среднюю зарплату по вакансиям.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as curs:
                curs.execute('SELECT company_name, ROUND(AVG(salary)) AS average_salary '
                             'FROM companies '
                             'JOIN vacancies USING (company_id) '
                             'GROUP BY company_name;')

                result = curs.fetchall()

        except (Exception, psycopg2.DatabaseError) as err:
            return err

        conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple] or str:
        """
        Получает список всех вакансий с зарплатой, превышающей среднюю по всем вакансиям.
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as curs:
                curs.execute('SELECT * FROM vacancies '
                             'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

                result = curs.fetchall()

        except (Exception, psycopg2.DatabaseError) as err:
            return err

        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple] or str:
        """
        Получает список всех вакансий, названия которых содержат слова, переданные в метод, например, python.
        :param keyword: строка с частью названия вакансии
        """
        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as curs:
                curs.execute(f"""
                SELECT * FROM vacancies
                WHERE lower(title_vacancy) LIKE '%{keyword}%'
                    OR lower(title_vacancy) LIKE '%{keyword}'
                    OR lower(title_vacancy) LIKE '{keyword}%'
                """)

                result = curs.fetchall()

        except (Exception, psycopg2.DatabaseError) as err:
            return err

        conn.close()
        return result
