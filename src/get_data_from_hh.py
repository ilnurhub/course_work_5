import requests


def get_company(keyword: str) -> dict:
    """
    Возвращает работодателя
    """
    params = {
        'text': keyword  # Текст фильтра. Должно быть название компании
    }
    responce = requests.get('https://api.hh.ru/employers', params=params)
    company = responce.json()
    return company


def get_vacancies_from_company(company: dict) -> list:
    """
    Возвращает список вакансий компании
    """
    responce = requests.get(company['items'][0]['vacancies_url'])
    vacancies = responce.json()['items']
    return vacancies


def get_company_data(company: dict) -> dict:
    """
    Возвращает данные о работодателе
    """
    responce = requests.get(company['items'][0]['url'])
    company_data = responce.json()
    return company_data


def format_salary_data(vacancy: dict) -> dict:
    """
    Возвращает отформатированные данные о зарплате
    """
    if vacancy['salary'] == None:
        vacancy['salary'] = {
            'from': 0,
            'to': 0
        }
    elif vacancy['salary']['from'] == None:
        vacancy['salary']['from'] = vacancy['salary']['to']
    elif vacancy['salary']['to'] == None:
        vacancy['salary']['to'] = vacancy['salary']['from']
    return vacancy
