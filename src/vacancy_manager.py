import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.vacancy import Vacancy


class VacancyManager(ABC):
    """Абстрактный класс для работы с JSON-файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancy(self, criteria: Any) -> List[Dict[str, Any]]:
        """Получить данные из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_url: str) -> None:
        """Удалить информацию о вакансии по URL"""
        pass


class JsonVacancyManager(VacancyManager):

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """Инициализация вакансий из JSON-файла"""
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w") as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в JSON-файл"""
        with open(self.__filename, "r+") as f:
            vacancies = json.load(f)
            vacancies.append(vacancy.dict)
            f.seek(0)
            f.truncate()
            json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def get_vacancy(self, criteria: Any) -> List[Dict[str, Any]]:
        """Получить данные из файла по указанным критериям"""
        with open(self.__filename, "r") as f:
            vacancies = json.load(f)
            filtered_vacancies = [v for v in vacancies if all(k in v and v[k] == criteria[k] for k in criteria)]
            return filtered_vacancies

    def delete_vacancy(self, vacancy_url: str) -> None:
        """Удалить информацию о вакансии по URL."""
        with open(self.__filename, "r+") as f:
            vacancies = json.load(f)
            vacancies = [v for v in vacancies if v.get("url") != vacancy_url]
            f.seek(0)
            f.truncate()
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
