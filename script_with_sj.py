import os
import requests
from dotenv import load_dotenv

load_dotenv()

def pages_count_hh(url, payload):
    response = requests.get(url, params=payload)
    pages_number = response.json()['pages']
    print(pages_number)
    return pages_number


def pages_count_sj(sj_url, headers, payload):
    response = requests.get(sj_url, headers=headers, params=payload)
    total_vacancy_number = response.json()['total']
    pages_number = int(int(total_vacancy_number)/ 20)
    print(pages_number)
    return pages_number


def count_salary_for_all_pages(pages_avarage_salary):
    sum_salary = 0
    for page_salary in pages_avarage_salary:
        sum_salary += page_salary
    avarage_salary = sum_salary/(len(pages_avarage_salary))
    return avarage_salary


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = (int(salary_to) + int(salary_to)) / 2
    elif salary_from is not None or salary_from == 0:
        average_salary = int(salary_from) * 1.2
    elif salary_to is not None or salary_to == 0:
        average_salary = int(salary_to) * 0.8
    print(average_salary)
    return average_salary


def get_hh_salaries(hh_url, payload, pages_number):
    vacancies_processed = 0
    pages_average_salary = []
    for number in range(pages_number):
        payload['page'] = number
        print(payload)
        response = requests.get(hh_url, params=payload)
        print(response.text)
        vacancies = response.json()['items']
        response.raise_for_status()
        for salary in vacancies:
            if not salary['salary']:
                continue
            elif salary['salary']['currency'] == 'RUR':
                salary_from = salary['salary']['from']
                salary_to = salary['salary']['to']
                average_salary = predict_salary(salary_from, salary_to)
                vacancies_processed += 1
                pages_average_salary.append(average_salary)
    return pages_average_salary, response, vacancies_processed


def get_sj_salaries(sj_url, headers, payload, pages_number):
    vacancies_processed = 0
    pages_average_salary = []
    print('страниц', range(pages_number))
    #for number in range(pages_number):
    more = True
    while more
        payload['page'] = number
        response = requests.get(sj_url, headers=headers, params=payload)
        more = response.json()['more']
        vacancies = response.json()['objects']
        response.raise_for_status()
        for salary in vacancies:
          if salary['currency'] == 'rub':
            salary_from = salary['payment_from']
            salary_to = salary['payment_to']
            average_salary = predict_salary(salary_from, salary_to)
            vacancies_processed += 1
            pages_average_salary.append(average_salary)
            print(average_salary)
        return pages_average_salary, response, vacancies_processed


def predict_rub_hh_salary(hh_url, payload, pages_number):
    vacancy_info = {}
    pages_average_salary, response, vacancies_processed = get_hh_salaries(hh_url, payload, pages_number)
    if len(pages_average_salary) != 0:
        average_salary = count_salary_for_all_pages(pages_average_salary)
        print('новая профессия', average_salary)
        vacancies_found = response.json()['found']
        vacancy_info['vacancies_found'] = vacancies_found
        vacancy_info['vacancies_processed'] = vacancies_processed
        vacancy_info['average_salary'] = int(average_salary)
        return vacancy_info


def predict_rub_sj_salary(sj_url, headers, payload, pages_number):
    vacancy_info = {}
    pages_average_salary, response, vacancies_processed = get_sj_salaries(sj_url, headers, payload, pages_number)
    if len(pages_average_salary) != 0:
        average_salary = count_salary_for_all_pages(pages_average_salary)
        vacancies_found = response.json()['total']
        print('страница', average_salary, 'найдено', pages_number)
        vacancy_info['vacancies_found'] = vacancies_found
        vacancy_info['vacancies_processed'] = vacancies_processed
        vacancy_info['average_salary'] = int(average_salary)
        return vacancy_info


def get_average_hh_salaries(hh_url, positions):
    vacancies_info = {}
    for position in positions:
        payload = {
            'text': position,
            'only_with_salary': 'true',
            'specialization': '1.221',
            'period': '31',
            'area': '1',
        }
        pages_mumber = pages_count_hh(hh_url, payload)
        vacancy_info = predict_rub_hh_salary(hh_url, payload, pages_mumber)
        vacancies_info[position] = vacancy_info
    return vacancies_info


def get_average_sj_salaries(sj_url, positions, sj_secret_key):
    headers = {
        'X-Api-App-Id': sj_secret_key
    }
    vacancies_info = {}
    for position in positions:
        payload = {
            'keyword': position,
            'catalogues': 48,
            'town': 4,
        }
        pages_number = pages_count_sj(sj_url, headers, payload)
        vacancy_info = predict_rub_sj_salary(sj_url, headers, payload, pages_number)
        vacancies_info[position] = vacancy_info
    return vacancies_info


def main():
    hh_url = 'https://api.hh.ru/vacancies'
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    sj_secret_key = os.getenv('SJ_TOKEN')
    positions = ['Программист JavaScript', 'Программист Java', 'Программист Python', 'Программист PHP',
                 'Программист C++', 'Программист C#', 'Программист C', 'Программист Swift']
    #hh_average_salaries = get_average_hh_salaries(hh_url, positions)
    sj_average_salaries = get_average_sj_salaries(sj_url, positions, sj_secret_key)
    print(sj_average_salaries)


if __name__ == '__main__':
    main()