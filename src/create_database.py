from configparser import ConfigParser
from typing import Any, Dict

import psycopg2
import requests


def create_database(database_name: str, params: dict) -> None:
    db_params = params.copy()
    db_params.pop("dbname", None)
    conn = psycopg2.connect(dbname="postgres", **db_params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
    finally:
        cur.close()
        conn.close()

    db_params["dbname"] = database_name

    conn = psycopg2.connect(**db_params)

    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancies")
            cur.execute("DROP TABLE IF EXISTS companies")
            cur.execute(
                """
                CREATE TABLE companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    url VARCHAR(255) NOT NULL
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE vacancies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    salary NUMERIC,
                    url VARCHAR(255) NOT NULL,
                    company_name VARCHAR(255) NOT NULL
                )
            """
            )
    finally:
        conn.commit()
        conn.close()


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params_i = parser.items(section)
        for param in params_i:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {section} is not found in the {filename} file.")
    return db


def insert_data_into_db(database_name: str, params: dict, companies_data: Dict[str, Any]) -> None:
    db_params = params.copy()
    db_params["dbname"] = database_name
    conn = psycopg2.connect(**db_params)

    with conn.cursor() as cur:
        for company_name, company_info in companies_data.items():
            if company_info:
                company_id = company_info["id"]
                company_url = company_info["alternate_url"]
                cur.execute(
                    """
                    INSERT INTO companies (id, name, url) VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """,
                    (company_id, company_name, company_url),
                )

                vacancies_url = company_info.get("vacancies_url")
                if vacancies_url:
                    page = 0
                    while True:
                        vacancies_response = requests.get(vacancies_url, params={"page": page, "per_page": 20})
                        if vacancies_response.status_code != 200:
                            break
                        vacancies_data = vacancies_response.json()
                        vacancies = vacancies_data.get("items", [])

                        if not vacancies:
                            break

                        for vacancy in vacancies:
                            title = vacancy.get("name")
                            salary = 0

                            if vacancy["salary"]:
                                salary_from = vacancy["salary"].get("from")
                                salary_to = vacancy["salary"].get("to")

                                if salary_from is not None and salary_to is not None:
                                    salary = (salary_from + salary_to) / 2
                                elif salary_from is not None:
                                    salary = salary_from
                                elif salary_to is not None:
                                    salary = salary_to

                            url = vacancy.get("alternate_url")
                            cur.execute(
                                """
                                INSERT INTO vacancies (title, salary, url, company_name)
                                VALUES (%s, %s, %s, %s)
                                """,
                                (title, salary, url, company_name),
                            )
                        page += 1

        conn.commit()
        conn.close()
