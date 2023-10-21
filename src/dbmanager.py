import psycopg2
from config import config


class DBManager:
    """
    Для работы с данными в БД.
    """

    def __init__(self):
        self.database_name = 'hh_vacancies'
        self.params = config()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.title, COUNT(*) FROM companies
                INNER JOIN vacancies 
                USING(company_id) 
                GROUP BY companies.title
                """
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.title, vacancies.title, (min_salary + max_salary) / 2, vacancy_url 
                FROM companies
                INNER JOIN vacancies 
                USING(company_id)
                """
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
        conn.close()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((min_salary + max_salary) / 2) FROM vacancies
                """
            )
            average_salary = cur.fetchone()
            print(f"Средняя зарплата по всем вакансиям: {int(average_salary[0])} руб")
        conn.close()
