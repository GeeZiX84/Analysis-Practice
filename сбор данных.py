import requests
import pandas as pd
import asyncio
import aiohttp
import numpy as np

# URL API
url = "https://api.hh.ru/vacancies"
professional_roles = ["116", "160", "114", "112"]
vacancies_list = []

async def fetch(session, url, params):
    async with session.get(url, params=params) as response:
        return await response.json()

async def fetch_vacancies():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for p in range(100):  # Количество страниц
            params = {
                "professional_role": professional_roles,
                "area": 1,
                "per_page": 100,  # Увеличение количества вакансий на странице
                "page": p
            }
            tasks.append(fetch(session, url, params))
        responses = await asyncio.gather(*tasks)
        return responses

def process_data(data):
    for page_data in data:
        if "items" in page_data:
            for vacancy in page_data["items"]:
                salary = vacancy.get("salary")
                if salary:
                    salary_from = salary.get("from")
                    salary_to = salary.get("to")
                    currency = salary.get("currency")
                    salary_str = f"{salary_from or ''} - {salary_to or ''} {currency or ''}".strip(" -")
                else:
                    salary_str = "Не указана"
                vacancies_list.append({
                    "Название": vacancy['name'],
                    "Компания": vacancy['employer']['name'],
                    "Требования": vacancy['snippet']['requirement'],
                    "Обязаности": vacancy['snippet']['responsibility'],
                    "Зарплата": salary_str,
                    "Опыт работы": vacancy["experience"]["name"],
                    "Ссылка": vacancy['alternate_url']
                })

data = asyncio.run(fetch_vacancies())
process_data(data)

# Преобразуем список в DataFrame
df = pd.DataFrame(vacancies_list)
df = df[~df["Название"].str.lower().str.startswith("продавец")]


# Выводим таблицу
def remove_last_ellipsis_sentence(text):
    if text == None:
        return
    else:
        sentences = text.split('. ')
        if sentences[-1].endswith('...'):
            sentences = sentences[:-1]
        return '. '.join(sentences)

df["Обязаности"] = df["Обязаности"].apply(remove_last_ellipsis_sentence)
df['Требования'] = df['Требования'].apply(remove_last_ellipsis_sentence)

# Выведем первые строки для анализа структуры данных
# Выводим таблицу

df.to_csv("dt.csv", index=False)
df.to_excel("dt.xlsx", index=False)


