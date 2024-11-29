import pytest

from src.vacancy import Vacancy


def test_initialization(vacancy_object):
    """Тестирование инициализации экземпляра Vacancy"""
    assert vacancy_object.title == "Программист Python"
    assert vacancy_object.url == "https://example.com/vacancy/1"
    assert vacancy_object.original_salary == "1000 – 1500"
    assert vacancy_object.salary == 1250  # Среднее от 1000 и 1500
    assert vacancy_object.description == "Разработка приложений на Python"


def test_invalid_initialization_without_title():
    """Тестирование инициализации без названия вакансии"""
    with pytest.raises(ValueError, match="Название вакансии не должно быть пустым."):
        Vacancy(title="", url="https://example.com/vacancy/2")


def test_invalid_initialization_without_url():
    """Тестирование инициализации без ссылки на вакансию"""
    with pytest.raises(ValueError, match="Ссылка на вакансию не должна быть пустой."):
        Vacancy(title="Программист Python", url="", salary=1000)


def test_negative_salary():
    """Тестирование валидации с отрицательной зарплатой"""
    with pytest.raises(ValueError, match="Зарплата не может быть отрицательной."):
        Vacancy(title="Программист", url="https://example.com", salary=-1000)


def test_parse_salary():
    """Тестирование метода parse_salary"""
    assert Vacancy.parse_salary(Vacancy, "2000") == 2000
    assert Vacancy.parse_salary(Vacancy, "1000 – 1500") == 1250
    assert Vacancy.parse_salary(Vacancy, None) == 0
    assert Vacancy.parse_salary(Vacancy, "abc") == 0


def test_dict_representation(vacancy_object):
    """Тестирование словарного представления экземпляра Vacancy"""
    expected_dict = {
        "title": "Программист Python",
        "url": "https://example.com/vacancy/1",
        "salary": "1000 – 1500",
        "description": "Разработка приложений на Python",
    }
    assert vacancy_object.dict == expected_dict


def test_cast_to_object_list():
    """Тестирование метода cast_to_object_list"""
    test_data = [
        {
            "name": "Программист Python",
            "alternate_url": "https://example.com/vacancy/1",
            "salary": {"from": 1000},
            "snippet": {"responsibility": "Кодирование"},
        },
        {
            "name": "Системный администратор",
            "alternate_url": "https://example.com/vacancy/2",
            "salary": {"from": 800},
            "snippet": {"responsibility": "Поддержка систем"},
        },
    ]
    vacancies = Vacancy.cast_to_object_list(test_data)
    assert len(vacancies) == 2
    assert vacancies[0].title == "Программист Python"
    assert vacancies[1].title == "Системный администратор"


def test_comparison_methods(vacancy_object):
    """Тестирование методов сравнения"""
    lower_vacancy = Vacancy(title="Младший программист", url="https://example.com/vacancy/3", salary=800)
    assert vacancy_object > lower_vacancy
    assert vacancy_object >= lower_vacancy
    assert vacancy_object != lower_vacancy
