from src.create_database import config, create_database, insert_data_into_db
from src.db_manager import DBManager
from src.hh_api import HHAPI
from src.user_interface import user_interface

#from src.job_api import HHAPI
# from src.vacancy import Vacancy
# from src.vacancy_manager import JsonVacancyManager
# from src.user_interaction import user_interaction

# hh_api = HHAPI()
# hh_vacancies = hh_api.get_vacancies("Python")
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
# json_saver = JsonVacancyManager()
# json_saver_1 = JsonVacancyManager("data/vacansies_1.json")
#
#
# # для работы с готовыми данными из main.py
# vacancy = Vacancy(
#     "Python Developer", "<https://hh.ru/vacancy/123456>", "100000-200000 руб.", "Требования: опыт работы от 3 лет..."
# )
# vacancy_1 = Vacancy("Developer", "<https://hh.ru/vacancy/132>", "150000 руб.", "Требования: опыт работы от 3 лет...")
# json_saver.add_vacancy(vacancy)
# json_saver.add_vacancy(vacancy_1)
# json_saver.delete_vacancy("<https://hh.ru/vacancy/123456>")
# if vacancy > vacancy_1:
#     print(f"{vacancy.title} имеет более высокую зарплату, чем {vacancy_1.title}.")
# elif vacancy < vacancy_1:
#     print(f"{vacancy_1.title} имеет более высокую зарплату, чем {vacancy.title}.")
# else:
#     print(f"Зарплата {vacancy_1.title} и {vacancy.title} равны.")
#
#
# # для работы с данными через api
# for vacancy in vacancies_list:
#     json_saver_1.add_vacancy(vacancy)
# result = json_saver_1.get_vacancy({"title": "Web-программист - стажер"})
# print(result)
#
# if __name__ == "__main__":
#     user_interaction()


def main():
    params = config()
    create_database("HH", params)

    db_manager = DBManager()
    db_manager.init({"dbname": "HH", **params})

    hh_api = HHAPI()
    company_names = [
        "Газпром автоматизация",
        "Газпром-Медиа",
        "Яндекс.Еда",
        "Skyeng",
        "Додо Пицца (Корпоративная розничная сеть)",
        "Welltex",
        "Doczilla",
        "Онлайн Касса.Ру",
        "Bazaar-tex",
        "ЭксИм Пасифик",
    ]

    companies_data = hh_api.fetch_companies(company_names)
    insert_data_into_db("HH", params, companies_data)

    # Запускаем пользовательский интерфейс
    user_interface(db_manager)


if __name__ == "__main__":
    main()
