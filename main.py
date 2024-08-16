from config import config
from src.entities import Name, Link, Salary, VacancyDescription, Employer, Address
from src.filemanager import DataBaseConnector
from src.parser import HHApiConnector, APIManager
from src.vacancy import Vacancy


def main():
    api_connection = HHApiConnector()
    connection_manager = APIManager(api_connection)
    vacancies_raw_data = connection_manager.api_connection()
    vacancy = Vacancy(Name, Link, Salary, VacancyDescription, Employer, Address)
    vacancies_processed_data = vacancy.create_vacancy(vacancies_raw_data)
    params = config()
    # print(params)
    # db_manager = DataBaseManager("vacancies", params)
    # db_connector = DataBaseConnector(db_manager)
    # db_connector.open_connection()
    # db_connector.db_manager.get_companies_and_vacancies_count()
    DataBaseConnector.create_database("vacancies", params)
    DataBaseConnector.fill_database(vacancies_processed_data, "vacancies", params)
    # return vacancies_processed_data


if __name__ == '__main__':
    main()

