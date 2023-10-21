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
                SELECT companies.title AS company_name, COUNT(*) AS count_of_vacancies FROM companies
                INNER JOIN vacancies 
                USING(company_id) 
                GROUP BY companies.title
                """
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
        conn.close()
