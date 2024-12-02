from src.job_api import HHAPI
from src.vacancy import Vacancy
from src.vacancy_manager import JsonVacancyManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    api = HHAPI()
    storage = JsonVacancyManager("data/vacancies_user.json")

    while True:
        print("1. Поиск вакансий")
        print("2. Топ N вакансий по зарплате")
        print("3. Вакансии по ключевому слову в описании")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = api.get_vacancies(query)
            for item in vacancies:
                salary_info = item.get("salary")
                salary = salary_info["from"] if salary_info and "from" in salary_info else 0

                vacancy = Vacancy(
                    title=item["name"],
                    url=item["alternate_url"],
                    salary=salary,
                    description=item.get("snippet", {}).get("responsibility", ""),
                )
                storage.add_vacancy(vacancy)

        elif choice == "2":
            while True:
                try:
                    N = int(input("Введите количество вакансий: "))
                    if N <= 0:
                        print("Пожалуйста, введите положительное число.")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите целое число.")

            vacancies = storage.get_vacancy("")
            vacancy_objects = [Vacancy(**vacancy) for vacancy in vacancies]
            top_vacancies = sorted(vacancy_objects, key=lambda v: v.salary, reverse=True)[:N]
            for v in top_vacancies:
                print(v)

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            vacancies = storage.get_vacancy("")
            vacancy_objects = [Vacancy(**vacancy) for vacancy in vacancies]
            filtered_vacancies = [
                v for v in vacancy_objects if v.description and keyword.lower() in v.description.lower()
            ]
            if filtered_vacancies:
                for v in filtered_vacancies:
                    print(v)
            else:
                print("Вакансии не найдены.")

        elif choice == "4":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")
