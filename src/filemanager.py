from abc import ABC, abstractmethod
import psycopg2
from psycopg2 import OperationalError
from config import config
from enum import Enum


class VacancyFields(Enum):
    NAME = 0
    LINK = 1
    PAY = 2
    EMPLOYER_INFO = 3
    DESCRIPTION = 4
    ADDRESS = 5


class BaseDataManager(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DataBaseManager(BaseDataManager):

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""SELECT DISTINCT(name), COUNT() FROM """)

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass


class DataBaseConnector:

    def __init__(self, db_manager: DataBaseManager):
        self.db_manager = db_manager
        self.connection = None
        self.cursor = None

    def open_connection(self):
        try:
            self.connection = psycopg2.connect(self.db_manager.db_name, **self.db_manager.params)
            self.cursor = self.connection.cursor()
            print(f"Connection to {self.db_manager.db_name} database is successful")
        except OperationalError as err:
            print(f"The error {err} is occurred.")
        return self.connection, self.cursor

    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def create_database(database_name: str, params: dict):
        try:
            connection = psycopg2.connect(dbname="postgres", **params)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
            cursor.execute(f"CREATE DATABASE {database_name}")
            connection.close()

            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE employers (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100),
                            link VARCHAR(100),
                            address VARCHAR(100) 
                           )""")

            cursor.execute("""CREATE TABLE vacancies (
                            vacancy_id SERIAL,
                            employer_id INT REFERENCES employers(id),
                            name VARCHAR(100),
                            link VARCHAR(100),
                            bottom_salary INT DEFAULT NULL,
                            top_salary INT DEFAULT NULL,
                            currency VARCHAR(10) DEFAULT NULL,
                            gross BOOLEAN DEFAULT NULL,
                            responsibilities TEXT,
                            requirements TEXT
                            )""")
            connection.commit()
            cursor.close()
            connection.close()
        except OperationalError as err:
            print(f"The error '{err}' occurred")

    @staticmethod
    def fill_database(vacancies: list, database_name: str, params: dict):
        connection = psycopg2.connect(dbname=database_name, **params)
        cursor = connection.cursor()
        for vacancy in vacancies:
            cursor.execute(
                f"INSERT INTO employers (name, link, address) VALUES ('{vacancy[VacancyFields.EMPLOYER_INFO.value].name}', '{vacancy[VacancyFields.EMPLOYER_INFO.value].url}', '{vacancy[VacancyFields.ADDRESS.value]}')")
            if vacancy[VacancyFields.PAY.value] == "Зарплата не указана":
                cursor.execute(
                    f"INSERT INTO vacancies (name, link, responsibilities, requirements) VALUES ('{vacancy[VacancyFields.NAME.value]}', '{vacancy[VacancyFields.LINK.value]}', '{vacancy[VacancyFields.DESCRIPTION.value].responsibility}', '{vacancy[VacancyFields.DESCRIPTION.value].requirement}')")
            else:
                cursor.execute(
                    f"INSERT INTO vacancies (name, link, bottom_salary, top_salary, currency, gross, responsibilities, requirements) VALUES ('{vacancy[VacancyFields.NAME.value]}', '{vacancy[VacancyFields.LINK.value]}', {vacancy[VacancyFields.PAY.value].bottom_salary}, {vacancy[VacancyFields.PAY.value].top_salary}, '{vacancy[VacancyFields.PAY.value].currency}', '{vacancy[VacancyFields.PAY.value].gross}', '{vacancy[VacancyFields.DESCRIPTION.value].responsibility}', '{vacancy[VacancyFields.DESCRIPTION.value].requirement}')")
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    # par = config()
    # print(par)
    # DataBaseConnector.create_database("vacancies", par)
    # DataBaseConnector.fill_database()
    print(VacancyFields.EMPLOYER_INFO.value)
