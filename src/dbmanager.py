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
            print('Cписок всех компаний и количество вакансий у каждой компании.')
            for row in rows:
                print(f"Компания: {row[0]} \nКоличество вакансий: {row[1]}\n")
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.title, vacancies.title, min_salary, max_salary, vacancy_url 
                FROM companies
                INNER JOIN vacancies 
                USING(company_id)
                """
            )
            rows = cur.fetchall()
            print('Список всех вакансий')
            for row in rows:
                print(
                    f"Компания: {row[0]} \nВакансия: {row[1]} \nЗарплата от: {row[2]} \nЗарплата до: {row[3]} "
                    f"\nСсылка на вакансию: {row[4]}\n")
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
            print(f"Средняя зарплата по всем вакансиям: {int(average_salary[0])} руб\n")
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.title, vacancies.title, (min_salary + max_salary) / 2, vacancy_url 
                FROM companies
                INNER JOIN vacancies 
                USING(company_id)
                WHERE (min_salary + max_salary) / 2 > (SELECT AVG((min_salary + max_salary) / 2) FROM vacancies)
                """
            )
            rows = cur.fetchall()
            print('Список всех вакансий, у которых зарплата выше средней по всем вакансиям.')
            for row in rows:
                print(
                    f"Компания: {row[0]} \nВакансия: {row[1]} \nСредняя зарплата: {row[2]} "
                    f"\nСсылка на вакансию: {row[3]}\n")
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT companies.title, vacancies.title, min_salary, max_salary, vacancy_url 
                FROM companies
                INNER JOIN vacancies 
                USING(company_id)
                WHERE vacancies.title ILIKE '%{keyword}%'
                """
            )
            rows = cur.fetchall()
            if not rows:
                print('Нет вакансий, соответствующих Вашему запросу')
            else:
                print(f'Список всех вакансий, в названии которых содержится слово {keyword}')
                for row in rows:
                    print(
                        f"Компания: {row[0]} \nВакансия: {row[1]} \nЗарплата от: {row[2]} \nЗарплата до: {row[3]} "
                        f"\nСсылка на вакансию: {row[4]}\n")
        conn.close()
