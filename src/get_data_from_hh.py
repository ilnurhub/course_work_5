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


def get_vacancies_from_company(company: str) -> list:
    """
    Возвращает список вакансий компании
    """
    responce = requests.get(company['items'][0]['vacancies_url'])
    vacancies = responce.json()['items']
    return vacancies
