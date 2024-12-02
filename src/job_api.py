from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import requests


class JobAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def connect(self) -> None:
        """Метод подключения к API в абстрактном классе"""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """Метод получения вакансий отдельно в абстрактном классе"""
        pass


class HHAPI(JobAPI):
    """Класс для работы с hh.ru"""

    __BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        """Инициализация нового объекта сессии для работы с API"""
        self.__session = requests.Session()

    def __connect(self) -> None:
        """Метод подключения к API"""
        pass

    def connect(self) -> None:
        """Публичный метод для вызова приватного"""
        self.__connect()

    def get_vacancies(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """Метод получения вакансий"""
        self.connect()
        params: Dict[str, Union[str, int]] = {"text": query, "per_page": per_page}
        response = self.__session.get(self.__BASE_URL, params=params)

        if response.status_code == 200:
            items = response.json().get("items", [])

            if isinstance(items, list):
                if all(isinstance(item, dict) for item in items):
                    return items
                else:
                    raise ValueError("Некоторые элементы не являются словарями.")
            else:
                raise ValueError("Ответ не содержит список 'items'.")
        else:
            raise Exception("Ошибка при запросе к API")
