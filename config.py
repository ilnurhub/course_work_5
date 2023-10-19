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


COMPANIES = ['ООО Томору', 'Skyeng', 'ООО Аптрейд', 'ООО Фабрика Решений', 'Hexlet', 'ООО АЙТИ.СПЕЙС', 'Газпромбанк',
             'Bell Integrator', 'ООО Кью Лаб', 'Сбер. IT']  # список из 10 компаний
