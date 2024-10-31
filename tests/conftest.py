import os

import pytest

from src.job_api import HHAPI
from src.vacancy import Vacancy
from src.vacancy_manager import JsonVacancyManager


@pytest.fixture
def hh_api():
    """Фикстура для создания экземпляра HHAPI."""
    api = HHAPI()
    api.__init__()
    return api


@pytest.fixture
def vacancy_data():
    """Фикстура для тестирования класса Vacancy"""
    return {
        "title": "Программист Python",
        "url": "https://example.com/vacancy/1",
        "salary": "1000 – 1500",
        "description": "Разработка приложений на Python",
    }


@pytest.fixture
def vacancy_object(vacancy_data):
    """Фикстура для создания экземпляра Vacancy"""
    return Vacancy(**vacancy_data)


@pytest.fixture
def vacancy_manager():
    """Фикстура для создания экземпляра JsonVacancyManager"""
    filename = "test_vacancies.json"
    manager = JsonVacancyManager(filename)
    yield manager
    os.remove(filename)


@pytest.fixture
def sample_vacancy():
    """Фикстура для создания образца вакансии"""
    return Vacancy(
        title="Программист Python",
        url="https://example.com/vacancy/1",
        salary="1000 – 1500",
        description="Разработка приложений на Python",
    )
