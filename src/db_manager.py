from typing import Any, Dict, List

import psycopg2


class DBManager:
    """Класс для управления подключением к базе данных и выполнения запросов."""

    def init(self, db_params: dict):
        """Инициализация класса DBManager."""

        self.connection = psycopg2.connect(**db_params)

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """Получает список компаний и количество вакансий для каждой компании."""

        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, COUNT(v.id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.name = v.company_name
                GROUP BY c.id
            """
            )
            result = cur.fetchall()
            return [{"company_name": row[0], "vacancies_count": row[1]} for row in result]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Получает все вакансии из базы данных."""

        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT v.title, v.salary, v.url, c.name AS company_name
                FROM vacancies v
                JOIN companies c ON v.company_name = c.name
            """
            )
            result = cur.fetchall()
            return [{"title": row[0], "salary": row[1], "url": row[2], "company_name": row[3]} for row in result]

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по всем вакансиям."""
        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary) FROM vacancies
            """
            )
            avg_salary = cur.fetchone()[0]
            return avg_salary if avg_salary is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Получает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT title, salary, url, company_name
                FROM vacancies
                WHERE salary > %s
            """,
                (avg_salary,),
            )
            result = cur.fetchall()
            return [{"title": row[0], "salary": row[1], "url": row[2], "company_name": row[3]} for row in result]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии, содержащие заданное ключевое слово в названии."""
        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT title, salary, url, company_name
                FROM vacancies
                WHERE TRIM(title) ILIKE %s OR TRIM(title) ILIKE %s;
            """,
                ("%" + keyword + "%", "%" + keyword.capitalize() + "%"),
            )
            result = cur.fetchall()
            return [{"title": row[0], "salary": row[1], "url": row[2], "company_name": row[3]} for row in result]

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()
