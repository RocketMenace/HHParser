from config import config
from src.entities import Name, Link, Salary, VacancyDescription, Employer, Address
from src.filemanager import DataBaseConnector, DataBaseManager
from src.parser import HHApiConnector, APIManager
from src.vacancy import Vacancy


def main():
    # api_connection = HHApiConnector()
    # connection_manager = APIManager(api_connection)
    # vacancies_raw_data = connection_manager.api_connection()
    # vacancy = Vacancy(Name, Link, Salary, VacancyDescription, Employer, Address)
    # vacancies_processed_data = vacancy.create_vacancy(vacancies_raw_data)
    params = config()
    db_manager = DataBaseManager("vacancies", params, cursor)
    db_connector = DataBaseConnector(db_manager)
    connection, cursor = db_connector.open_connection()
    print(db_connector.db_manager.get_companies_and_vacancies_count())
    db_connector.close_connection()
    # DataBaseConnector.create_database("vacancies", params)
    # DataBaseConnector.fill_employers(vacancies_processed_data, "vacancies", params)
    # DataBaseConnector.fill_vacancies(vacancies_processed_data, "vacancies", params)
    # return vacancies_processed_data


if __name__ == '__main__':
    main()


