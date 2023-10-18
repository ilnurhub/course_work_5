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
