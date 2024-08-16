from abc import ABC, abstractmethod


class BaseVacancy(ABC):

    @abstractmethod
    def create_vacancy(self, vacancies: list[dict]):
        pass


class Vacancy(BaseVacancy):
    name: str
    link: str
    pay: str
    description: str
    employer_info: str

    def __init__(self, name, link, pay, description, employer_info, address):
        self.employer_info = employer_info
        self.description = description
        self.pay = pay
        self.link = link
        self.name = name
        self.address = address

    def create_vacancy(self, vacancies: list[dict]):
        steps = (self.name.create_entity,
                 self.link.create_entity,
                 self.pay.create_entity,
                 self.employer_info.create_entity,
                 self.description.create_entity,
                 self.address.create_entity)
        return [[step(vacancy) for step in steps] for vacancy in vacancies]

    def __repr__(self):
        return f"{self.name}. {self.link}. {self.pay}. {self.description}. {self.employer_info}."



