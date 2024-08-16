from abc import ABC, abstractmethod
from typing import Any
import re


class AbstractEntity(ABC):

    @classmethod
    @abstractmethod
    def create_entity(cls, *args, **kwargs):
        pass


class Name(AbstractEntity):
    name: str

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        name = vacancy.get("name", "не указано")
        return cls(name)

    def __repr__(self):
        return f"{self.name}"


class Link(AbstractEntity):
    url: str

    def __init__(self, url):
        self.url = url

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        url = vacancy.get("alternate_url", "не указано")
        return cls(url)

    def __repr__(self):
        return f"{self.url}"


class Salary(AbstractEntity):
    gross: bool
    currency: str
    top_salary: int
    bottom_salary: int

    def __init__(self, gross, currency, top_salary, bottom_salary):
        self.gross = gross
        self.currency = currency
        self.top_salary = top_salary
        self.bottom_salary = bottom_salary

    @property
    def bottom_salary(self):
        return self._bottom_salary

    @bottom_salary.setter
    def bottom_salary(self, value):
        if not value:
            self._bottom_salary = 0
        else:
            self._bottom_salary = value

    @property
    def top_salary(self):
        return self._top_salary

    @top_salary.setter
    def top_salary(self, value):
        if not value:
            self._top_salary = 0
        else:
            self._top_salary = value

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        salary = vacancy.get("salary")
        if not salary:
            return "Зарплата не указана"
        gross = salary.get(
            "gross",
        )
        currency = salary.get("currency")
        top_salary = salary.get("to")
        bottom_salary = salary.get("from")
        return cls(gross, currency, top_salary, bottom_salary)

    def __repr__(self):
        if not self.gross:
            return f"Заработная плата в {self.currency} до вычета налогов от {self._bottom_salary} -> до {self._top_salary}."
        return f"Заработная плата в {self.currency} за вычетом налогов от {self._bottom_salary} -> до {self._top_salary}."


class VacancyDescription(AbstractEntity):
    responsibility: str
    requirement: str

    def __init__(self, responsibility, requirement):
        self.responsibility = responsibility
        self.requirement = requirement

    @property
    def requirement(self):

        html_pattern = re.compile("<.*?>")
        edited = re.sub(html_pattern, "", self._requirement)
        return edited.replace("'", " ")

    @requirement.setter
    def requirement(self, value):
        if value:
            self._requirement = value
        else:
            self._requirement = "не указаны"

    @property
    def responsibility(self):
        html_pattern = re.compile("<.*?>")
        return re.sub(html_pattern, "", self._responsibility)

    @responsibility.setter
    def responsibility(self, value):
        if value:
            self._responsibility = value
        else:
            self._responsibility = "не указаны"

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        description = vacancy.get("snippet")
        responsibility = description.get("responsibility")
        requirement = description.get("requirement")
        return cls(responsibility, requirement)

    def __repr__(self):
        return f"{self.responsibility} {self.requirement}"


class Address(AbstractEntity):

    def __init__(self, city: str, street: str, building: str):
        self.city = city
        self.street = street
        self.building = building

    @classmethod
    def create_entity(cls, vacancy: dict[str: Any]):
        address = vacancy.get("address")
        if not address:
            return 'Адрес не указан'
        city = address.get("city")
        street = address.get("street")
        building = address.get("building")
        return cls(city, street, building)

    def __repr__(self):
        return f"г. {self.city}, ул. {self.street}, стр. {self.building}"


class Employer(AbstractEntity):

    def __init__(self, url: str, name: str, employer_id: str):
        self.url = url
        self.name = name
        self.employer_id = employer_id

    @classmethod
    def create_entity(cls, vacancy: dict[str:Any]):
        employer = vacancy.get("employer")
        url = employer.get("alternate_url")
        name = employer.get("name")
        employer_id = employer.get("id")
        return cls(url, name, employer_id)

    def __repr__(self):
        return f"{self.name} {self.url}"



