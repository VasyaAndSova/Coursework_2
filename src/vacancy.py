class Vacancy:
    def __init__(self, title, url, salary=None, description=""):
        self.title = title
        self.url = url
        self.salary = salary if salary is not None else 0
        self.description = description

        self.validate()

    def validate(self):
        if not self.title:
            raise ValueError("Название вакансии не должно быть пустым.")
        if not self.url:
            raise ValueError("Ссылка на вакансию не должна быть пустой.")
        if self.salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        if not isinstance(self.salary, (int, float)):
            raise ValueError("Зарплата должна быть числом.")

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

