import psycopg2


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                site_url TEXT,
                hh_url TEXT,
                logo_url TEXT,
                fields_of_activity TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(company_id),
                title VARCHAR NOT NULL,
                publish_date DATE,
                min_salary INT NOT NULL,
                max_salary INT NOT NULL,
                requirement TEXT,
                experience TEXT,
                shedule TEXT,
                employment TEXT,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()
