from abc import ABC, abstractmethod
import json
import os

class VacancyManager(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавить вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """Получить данные из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """Удалить информацию о вакансии по ID."""
        pass

class JsonVacancyManager(VacancyManager):

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def add_vacancy(self, vacancy):
        """Добавить вакансию в JSON-файл."""
        with open(self.filename, 'r+') as f:
            vacancies = json.load(f)
            vacancies.append(vacancy)
            f.seek(0)
            json.dump(vacancies, f, indent=4)

    def get_vacancies(self, criteria):
        """Получить данные из файла по указанным критериям."""
        with open(self.filename, 'r') as f:
            vacancies = json.load(f)
            filtered_vacancies = [v for v in vacancies if all(k in v and v[k] == criteria[k] for k in criteria)]
            return filtered_vacancies

    def delete_vacancy(self, vacancy_id):
        """Удалить информацию о вакансии по ID."""
        with open(self.filename, 'r+') as f:
            vacancies = json.load(f)
            vacancies = [v for v in vacancies if v.get('id') != vacancy_id]
            f.seek(0)
            f.truncate()
            json.dump(vacancies, f, indent=4)