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

    def __init__(self, db_name: str, params: dict, cursor):
        self.db_name = db_name
        self.params = params
        self.cursor = cursor

    def get_companies_and_vacancies_count(self):
        result = self.cursor.execute("""SELECT employers.name, COUNT(*) AS total_vacancies FROM employers
                            JOIN vacancies ON vacancies.employer_id = employers.id
                            GROUP BY employers.name""")
        return result

    def get_all_vacancies(self):
        result = self.cursor.execute("""SELECT employers.name AS employer_name, vacancies.name 
                                    AS vacancy_name , top_salary, vacancies.link AS vacancy_link FROM employers
                                    JOIN vacancies ON vacancies.employer_id = employers.id
                                    WHERE top_salary IS NOT NULL
                                    ORDER BY top_salary DESC""")

    def get_avg_salary(self):
        result = self.cursor.execute("""SELECT name, AVG(top_salary)::numeric(10,2) AS avg_salary FROM vacancies
                                    WHERE top_salary IS NOT NULL
                                    GROUP BY name, top_salary
                                    ORDER BY top_salary DESC""")

    def get_vacancies_with_higher_salary(self):
        result = self.cursor.execute("""SELECT * FROM vacancies
                                    WHERE top_salary > (SELECT AVG(top_salary) FROM vacancies)
                                    ORDER BY top_salary DESC""")

    def get_vacancies_with_keyword(self):
        result = self.cursor.execute("""SELECT * FROM vacancies
                                    WHERE name LIKE '%Python%'""")


class DataBaseConnector:

    def __init__(self, db_manager: DataBaseManager):
        self.db_manager = db_manager
        self.connection = None
        self.cursor = None

    def open_connection(self):
        try:
            self.connection = psycopg2.connect(dbname=self.db_manager.db_name, **self.db_manager.params)
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
                            id INT PRIMARY KEY,
                            name VARCHAR(100),
                            link VARCHAR(100),
                            address VARCHAR(100) 
                           )""")

            cursor.execute("""CREATE TABLE vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            employer_id INT,
                            name VARCHAR(100),
                            link VARCHAR(100),
                            bottom_salary INT DEFAULT NULL,
                            top_salary INT DEFAULT NULL,
                            currency VARCHAR(10) DEFAULT NULL,
                            gross BOOLEAN DEFAULT NULL,
                            responsibilities TEXT,
                            requirements TEXT,
                            CONSTRAINT fk_employer_id FOREIGN KEY(employer_id) REFERENCES employers(id)
                            )""")
            connection.commit()
            cursor.close()
            connection.close()
        except OperationalError as err:
            print(f"The error '{err}' occurred")

    @staticmethod
    def fill_employers(vacancies: list, database_name: str, params: dict):
        connection = psycopg2.connect(dbname=database_name, **params)
        cursor = connection.cursor()
        company_names = set()
        for vacancy in vacancies:
            if vacancy[VacancyFields.EMPLOYER_INFO.value].name not in company_names:
                cursor.execute(
                    f"INSERT INTO employers (id, name, link, address) VALUES "
                    f"('{vacancy[VacancyFields.EMPLOYER_INFO.value].employer_id}', "
                    f"'{vacancy[VacancyFields.EMPLOYER_INFO.value].name}', "
                    f"'{vacancy[VacancyFields.EMPLOYER_INFO.value].url}', "
                    f"'{vacancy[VacancyFields.ADDRESS.value]}')")
            company_names.add(vacancy[VacancyFields.EMPLOYER_INFO.value].name)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def fill_vacancies(vacancies: list, database_name: str, params: dict):
        connection = psycopg2.connect(dbname=database_name, **params)
        cursor = connection.cursor()
        for vacancy in vacancies:
            if vacancy[VacancyFields.PAY.value] == "Зарплата не указана":
                cursor.execute(
                    f"INSERT INTO vacancies (employer_id, name, link, responsibilities, requirements) VALUES "
                    f"('{vacancy[VacancyFields.EMPLOYER_INFO.value].employer_id}', "
                    f"'{vacancy[VacancyFields.NAME.value]}', "
                    f"'{vacancy[VacancyFields.LINK.value]}', "
                    f"'{vacancy[VacancyFields.DESCRIPTION.value].responsibility}', "
                    f"'{vacancy[VacancyFields.DESCRIPTION.value].requirement}')")
            else:
                cursor.execute(
                    f"INSERT INTO vacancies "
                    f"(employer_id, name, link, bottom_salary, top_salary, currency, gross, responsibilities, requirements) "
                    f"VALUES ('{vacancy[VacancyFields.EMPLOYER_INFO.value].employer_id}', "
                    f"'{vacancy[VacancyFields.NAME.value]}', "
                    f"'{vacancy[VacancyFields.LINK.value]}', "
                    f"{vacancy[VacancyFields.PAY.value].bottom_salary}, "
                    f"{vacancy[VacancyFields.PAY.value].top_salary}, "
                    f"'{vacancy[VacancyFields.PAY.value].currency}', "
                    f"'{vacancy[VacancyFields.PAY.value].gross}', "
                    f"'{vacancy[VacancyFields.DESCRIPTION.value].responsibility}', "
                    f"'{vacancy[VacancyFields.DESCRIPTION.value].requirement}')")
        connection.commit()
        cursor.close()
        connection.close()
