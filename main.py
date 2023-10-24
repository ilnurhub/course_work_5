from src.get_data_from_hh import get_company, get_company_data, get_vacancies_from_company, format_salary_data
from config import config, COMPANIES, MENU, DATABASE_NAME
from src.create_fill_db import create_database, save_data_to_database
from src.dbmanager import DBManager


def main():
    params = config()
    create_database(DATABASE_NAME, params)
    for company_name in COMPANIES:
        company = get_company(company_name)
        vacancies = get_vacancies_from_company(company)
        for vacancy in vacancies:
            format_salary_data(vacancy)
        company_data = get_company_data(company)
        save_data_to_database(company_data, vacancies, DATABASE_NAME, params)

    dbm = DBManager()

    choose = input(MENU)
    while choose != 0:
        if choose == '1':
            dbm.get_companies_and_vacancies_count()
            choose = input(MENU)
        elif choose == '2':
            dbm.get_all_vacancies()
            choose = input(MENU)
        elif choose == '3':
            dbm.get_avg_salary()
            choose = input(MENU)
        elif choose == '4':
            dbm.get_vacancies_with_higher_salary()
            choose = input(MENU)
        elif choose == '5':
            keyword = input('Введите ключевое слово, которое должно содержаться в названии вакансии: ')
            dbm.get_vacancies_with_keyword(keyword)
            choose = input(MENU)
        elif choose == '0':
            break
        else:
            print('Неверный ввод')
            choose = input(MENU)


if __name__ == '__main__':
    main()
