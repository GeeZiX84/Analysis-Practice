import requests
import time

def get_vacancies(skill, pages=1):
    all_skills = []
    professional_roles = ["116", "160", "114", "112"]
    for page in range(pages):
        params = {
                "professional_role": professional_roles,
                "area": 1,
                "per_page": 20,  # Увеличение количества вакансий на странице
                "page": page
            }

        response = requests.get('https://api.hh.ru/vacancies', params=params)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            continue

        data = response.json()

        for item in data['items']:
            vacancy_id = item['id']
            vacancy_response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
            if vacancy_response.status_code != 200:
                continue

            vacancy_data = vacancy_response.json()

            skills = [s['name'] for s in vacancy_data.get('key_skills', [])]
            all_skills.extend(skills)

        time.sleep(0.5)  # чтобы не словить бан

    return all_skills

if __name__ == "__main__":
    skill_to_search = 'Python'
    found_skills = get_vacancies(skill_to_search, pages=2)

    print("Найденные навыки:")
    for s in set(found_skills):
        print(f"- {s}")

print(found_skills)