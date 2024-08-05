from abc import ABC, abstractmethod

class BaseParser(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass