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
                fields_of_activity TEXT,
                site_url TEXT,
                hh_url TEXT,
                logo_url TEXT
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


def save_data_to_database(company_data: dict, vacancies: list, database_name: str, params: dict):
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO companies (title, site_url, hh_url, logo_url, fields_of_activity)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING company_id
            """,
            (company_data['name'], company_data['site_url'], company_data['alternate_url'],
             company_data['logo_urls']['original'], '. '.join(x['name'] for x in company_data['industries']))
        )
        company_id = cur.fetchone()[0]
        for vacancy in vacancies:
            cur.execute(
                """INSERT INTO vacancies (company_id, title, publish_date, min_salary, max_salary, requirement, 
                experience, shedule, employment, vacancy_url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (company_id, vacancy['name'], vacancy['published_at'], vacancy['salary']['from'],
                 vacancy['salary']['to'], vacancy['snippet']['requirement'], vacancy['experience']['name'],
                 vacancy['schedule']['name'], vacancy['employment']['name'], vacancy['alternate_url'])
            )
    conn.commit()
    conn.close()
