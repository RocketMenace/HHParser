from abc import ABC, abstractmethod
from typing import Any


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
        url = vacancy.get("url", "не указано")
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
            self._bottom_salary = "не указано"
        else:
            self._bottom_salary = value

    @property
    def top_salary(self):
        return self._top_salary

    @top_salary.setter
    def top_salary(self, value):
        if not value:
            self._top_salary = "не указано"
        else:
            self._top_salary = value

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        salary = vacancy.get("salary")
        if not salary:
            return f"Зарплата не указана"
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

    @classmethod
    def create_entity(cls, vacancy: dict[str, Any]):
        description = vacancy.get("snippet")
        responsibility = description.get("responsibility")
        requirement = description.get("requirement")
        return cls(responsibility, requirement)

    def __repr__(self):
        return f"{self.responsibility} {self.requirement}"


class Employer(AbstractEntity):
    url: str
    name: str

    def __init__(self, url, name):
        self.url = url
        self.name = name

    @classmethod
    def create_entity(cls, vacancy: dict[str:Any]):
        employer = vacancy.get("employer")
        url = employer.get("url")
        name = employer.get("name")
        return cls(url, name)

    def __repr__(self):
        return f"{self.name} {self.url}"



