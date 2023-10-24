from configparser import ConfigParser
from os import path

ROOT_PATH = path.dirname(path.abspath(__file__))


def config(filename=path.join(ROOT_PATH, "database.ini"), section="postgresql") -> dict:
    """
    Производит парсинг данных из файла database.ini
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


COMPANIES = ['ООО Томору', 'Skyeng', 'amoCRM', '«РОСБАНК»', 'Hexlet', 'ООО АЙТИ.СПЕЙС', 'Газпромбанк',
             'Bell Integrator', 'ООО Кью Лаб', 'Сбер. IT']  # список из 10 компаний

MENU = f"""
Меню:
1 - список всех компаний и количество вакансий у каждой компании.
2 - список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3 - средняя зарплата по вакансиям.
4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5 - список всех вакансий, в названии которых содержится ключевое слово, например python.
0 - выход
Выберите цифру: """

DATABASE_NAME = 'hh_vacancies'

COUNT_OF_VACANCIES_IN_PAGE = 100
