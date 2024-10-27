from abc import ABC, abstractmethod
import requests

class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query: str):
        pass


class HHAPI(JobAPI):
    BASE_URL = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, query: str):
        params = {'text': query}
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise Exception("Ошибка при запросе к API")