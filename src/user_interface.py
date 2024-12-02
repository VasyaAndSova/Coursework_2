from src.db_manager import DBManager


def user_interface(db_manager: DBManager):
    while True:
        print("\nВыберите опцию:")
        print("1. Показать компании и количество их вакансий")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату по вакансиям")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Показать вакансии по ключевому слову")
        print("0. Выход из системы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            companies_vacancies = db_manager.get_companies_and_vacancies_count()
            print("\nСписок компаний и количество их вакансий:")
            for company in companies_vacancies:
                print(f"{company['company_name']}: {company['vacancies_count']} вакансий")

        elif choice == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for vacancy in all_vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, "
                    f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {avg_salary}")

        elif choice == "4":
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vacancy in higher_salary_vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, "
                    f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска в названии вакансии: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии, содержащие '{keyword}' в названии:")
            for vacancy in keyword_vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, "
                    f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "0":
            print("Выход из системы.")
            break

        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")
