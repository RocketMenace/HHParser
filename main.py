from config import config
from src.entities import Name, Link, Salary, VacancyDescription, Employer, Address
from src.databasemanager import DataBaseConnector, DataBaseManager
from src.parser import HHApiConnector, APIManager
from src.vacancy import Vacancy


def main():
    """Function for interacting with user"""

    # Создаем экземпляр класса HHApiConnector для взаимодействия с API HeadHunter.
    api_connection = HHApiConnector()
    # Используя коннектор и менеджер соединений, извлекаем данные из API HeadHunter для дальнейшей обработки.
    connection_manager = APIManager(api_connection)
    vacancies_raw_data = connection_manager.api_connection()
    vacancy = Vacancy(Name, Link, Salary, VacancyDescription, Employer, Address)
    vacancies_processed_data = vacancy.create_vacancy(vacancies_raw_data)
    params = config()
    # Подготавливаем базы данных для хранения полученных данных.
    DataBaseConnector.create_database("vacancies", params)
    DataBaseConnector.fill_employers(vacancies_processed_data, "vacancies", params)
    DataBaseConnector.fill_vacancies(vacancies_processed_data, "vacancies", params)
    db_manager = DataBaseManager("vacancies", params)
    # Используем коннектор для создания подключения к базе данных.
    db_connector = DataBaseConnector(db_manager)
    connection, cursor = db_connector.open_connection()
    connection_is_active = True

    while connection_is_active:
        available_functions = {"1": db_connector.db_manager.get_companies_and_vacancies_count,
                               "2": db_connector.db_manager.get_all_vacancies,
                               "3": db_connector.db_manager.get_avg_salary,
                               "4": db_connector.db_manager.get_vacancies_with_higher_salary,
                               "5": db_connector.db_manager.get_vacancies_with_keyword}
        print("Доступные операции:",
              "1 - Список вакансий для каждой компании.",
              "2 - Список всех вакансий.",
              "3 - Средняя зарплата по всем вакансиям",
              "4 - Список вакансий с зарплатой выше средней.",
              "5 - Список вакансий c ключевым словом.",
              "0 - Завершение работы программы", sep='\n')
        operation = input("Введите номер необходимой операции из предложенных: ")
        if operation == "0":
            connection_is_active = False
        if operation == "5":
            available_functions[operation](cursor, keyword=input("Введите слово: "))
        else:
            available_functions[operation](cursor)
    db_connector.close_connection()


if __name__ == '__main__':
    main()
