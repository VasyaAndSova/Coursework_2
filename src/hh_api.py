from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class JobAPI(ABC):
    """Абстрактный базовый класс для API работы с вакансиями."""

    @abstractmethod
    def fetch_companies(self, company_names: List[str]) -> Dict[str, Any]:
        """Получает информацию о компаниях по их названиям."""
        pass


class HHAPI(JobAPI):
    """Класс для взаимодействия с API HeadHunter (hh.ru).
    Этот класс реализует методы для получения информации о работодателях через API HeadHunter."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        """Инициализирует сессию для выполнения запросов к API.
        Создает объект сессии requests.Session для управления соединениями."""

        self.session = requests.Session()

    def fetch_companies(self, company_names: List[str]) -> Dict[str, Any]:
        """Получает информацию о компаниях по их названиям через API HeadHunter."""

        companies_data = {}
        for company_name in company_names:
            response = self.session.get(f"{self.BASE_URL}/employers", params={"text": company_name, "per_page": 10})
            if response.status_code == 200:
                items = response.json().get("items", [])
                companies_data[company_name] = items[0] if items else None
            else:
                companies_data[company_name] = None
        return companies_data
