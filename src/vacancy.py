import re
from typing import Any, Dict, List, Optional, Union


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("title", "url", "original_salary", "salary", "description")

    def __init__(self, title: str, url: str, salary: Optional[Union[int, str]] = None, description: str = "") -> None:
        """Инициализация экземпляров вакансий"""
        self.title = title
        self.url = url
        self.original_salary: Optional[Union[int, str]] = salary
        self.salary = self.parse_salary(salary)
        self.description = description

        self.__validate()

    def __str__(self) -> str:
        """Реализация строкового представления объектов класса"""
        return f"Название вакансии: {self.title}; Зарплата: {self.salary}; Ссылка на вакансию: {self.url}"

    def parse_salary(self, salary: Optional[Union[int, str]]) -> Any:
        """Преобразование строки зарплаты в число"""
        if salary is None:
            return 0
        if isinstance(salary, int):
            return salary
        if isinstance(salary, str):
            numbers = re.findall(r"\d+", salary)
            if not numbers:
                return 0
            numbers = [int(num.replace(" ", "")) for num in numbers]
            if len(numbers) > 1:
                return sum(numbers) // len(numbers)
            else:
                return numbers[0]
        return 0

    def __validate(self) -> None:
        """Метод валидации данных"""
        if not self.title:
            raise ValueError("Название вакансии не должно быть пустым.")
        if not self.url:
            raise ValueError("Ссылка на вакансию не должна быть пустой.")
        if self.salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        if not isinstance(self.salary, (int, float)):
            raise ValueError("Зарплата должна быть числом.")

    @property
    def dict(self) -> Dict[str, Union[str, Optional[Union[int, str]]]]:
        """Создает словарь с атрибутами класса"""
        return {"title": self.title, "url": self.url, "salary": self.original_salary, "description": self.description}

    @staticmethod
    def cast_to_object_list(vacancies_data: Any) -> List["Vacancy"]:
        """Преобразует полученные данные в список объектов класса"""
        return [
            Vacancy(
                title=item["name"],
                url=item["alternate_url"],
                salary=item.get("salary", {}).get("from", 0) if item.get("salary") else 0,
                description=item.get("snippet", {}).get("responsibility", ""),
            )
            for item in vacancies_data
        ]

    # Магические методы сравнения
    def __lt__(self, other: "Vacancy") -> Any:
        return self.salary < other.salary

    def __le__(self, other: "Vacancy") -> Any:
        return self.salary <= other.salary

    def __gt__(self, other: "Vacancy") -> Any:
        return self.salary > other.salary

    def __ge__(self, other: "Vacancy") -> Any:
        return self.salary >= other.salary
