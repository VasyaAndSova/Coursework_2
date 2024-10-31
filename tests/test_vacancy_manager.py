import json
import os

from src.vacancy_manager import JsonVacancyManager


def test_add_vacancy(vacancy_manager, sample_vacancy):
    """Тестирование добавления вакансии"""
    vacancy_manager.add_vacancy(sample_vacancy)
    with open(vacancy_manager._JsonVacancyManager__filename, "r") as f:
        vacancies = json.load(f)
        assert len(vacancies) == 1
        assert vacancies[0]["title"] == sample_vacancy.title


def test_get_vacancy(vacancy_manager, sample_vacancy):
    """Тестирование получения вакансии по критериям"""
    vacancy_manager.add_vacancy(sample_vacancy)
    criteria = {"title": "Программист Python"}
    result = vacancy_manager.get_vacancy(criteria)
    assert len(result) == 1
    assert result[0]["url"] == sample_vacancy.url


def test_delete_vacancy(vacancy_manager, sample_vacancy):
    """Тестирование удаления вакансии по URL"""
    vacancy_manager.add_vacancy(sample_vacancy)
    vacancy_manager.delete_vacancy(sample_vacancy.url)

    with open(vacancy_manager._JsonVacancyManager__filename, "r") as f:
        vacancies = json.load(f)
        assert len(vacancies) == 0


def test_get_vacancy_no_results(vacancy_manager):
    """Тестирование получения вакансии при отсутствии результатов"""
    criteria = {"title": "Несуществующая Вакансия"}
    result = vacancy_manager.get_vacancy(criteria)
    assert result == []


def test_delete_vacancy_not_found(vacancy_manager, sample_vacancy):
    """Тестирование удаления вакансии, которая не существует"""
    vacancy_manager.add_vacancy(sample_vacancy)
    vacancy_manager.delete_vacancy("https://example.com/vacancy/not_found")

    with open(vacancy_manager._JsonVacancyManager__filename, "r") as f:
        vacancies = json.load(f)
        assert len(vacancies) == 1


def test_initialization_of_non_existent_file():
    """Тестирование инициализации несуществующего файла"""
    filename = "non_existent_file.json"
    manager = JsonVacancyManager(filename)
    assert os.path.exists(filename)
    os.remove(filename)
