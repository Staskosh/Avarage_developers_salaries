import os
from itertools import count

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if not salary_from and salary_to:
        return salary_to * 0.8
    elif salary_from and not salary_to:
        return salary_from * 1.2
    elif salary_to and salary_from:
        return (salary_from + salary_to) / 2


def calculate_sj_salary(salary, salary_sum, vacancies_processed):
    salary_from = salary['payment_from']
    salary_to = salary['payment_to']
    predicted_salary = predict_salary(salary_from, salary_to)
    if predicted_salary:
        salary_sum += predicted_salary
        vacancies_processed += 1
    return salary_sum, vacancies_processed


def get_sj_salaries(sj_secret_key, position):
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    development_and_programing = 48
    Moscow = 4
    headers = {
        'X-Api-App-Id': sj_secret_key
    }
    payload = {
        'keyword': position,
        'catalogues': development_and_programing,
        'town': Moscow,
    }
    salary_sum = 0
    vacancies_processed = 0
    for page_number in count(0):
        payload['page'] = page_number
        response = requests.get(sj_url, headers=headers, params=payload)
        response.raise_for_status()
        page = response.json()
        vacancies = page['objects']
        for salary in vacancies:
            if not salary['currency'] == 'rub':
                continue
            salary_sum, vacancies_processed = calculate_sj_salary(salary, salary_sum, vacancies_processed)
        if not page['more']:
            break
    vacancies_found = page['total']
    return salary_sum, vacancies_processed, vacancies_found


def calculate_hh_salary(salary, salary_sum, vacancies_processed):
    salary_from = salary['salary']['from']
    salary_to = salary['salary']['to']
    predicted_salary = predict_salary(salary_from, salary_to)
    if predicted_salary:
        salary_sum += predicted_salary
        vacancies_processed += 1
    return salary_sum, vacancies_processed

def get_hh_salary(position):
    hh_url = 'https://api.hh.ru/vacancies'
    development_programing = '1.221'
    month = '31'
    Moscow  = '1'
    payload = {
        'text': position,
        'specialization': development_programing,
        'period': month,
        'area': Moscow,
    }
    salary_sum = 0
    vacancies_processed = 0
    for page_number in count(0):
        payload['page'] = page_number
        print(page_number)
        response = requests.get(hh_url, params=payload)
        response.raise_for_status()
        page = response.json()
        vacancies = page['items']
        total_pages = page['pages']
        for salary in vacancies:
            if not salary['salary'] or not salary['salary']['currency'] == 'RUR':
                continue
            salary_sum, vacancies_processed = calculate_hh_salary(salary, salary_sum, vacancies_processed)
        if page_number > total_pages or page_number >= 99:
            break
    vacancies_found = page['found']
    return salary_sum, vacancies_processed, vacancies_found


def get_average_hh_salaries(positions):
    vacancies_info = {}
    for position in positions:
        salary_sum, vacancies_processed, vacancies_found = get_hh_salary(position)
        vacancies_info[position] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(salary_sum / vacancies_processed)
        }
    return vacancies_info


def get_average_sj_salaries(positions, sj_secret_key):
    vacancies_info = {}
    for position in positions:
        salary_sum, vacancies_processed, vacancies_found = get_sj_salaries(sj_secret_key, position)
        vacancies_info[position] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(salary_sum / vacancies_processed)
        }
    return vacancies_info


def print_tables(sj_average_salaries, source):
    table_data = [
        [source, 'Moscow'],
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ],
    ]
    for position, salary in sj_average_salaries.items():
        position_salariy = [
            position,
            salary['vacancies_found'],
            salary['vacancies_processed'],
            salary['average_salary'],
        ]
        table_data.append(position_salariy)
    table = AsciiTable(table_data)
    print(table.table)


def main():
    load_dotenv()
    positions = [
        'Программист JavaScript', 'Программист Java',
        'Программист Python', 'Программист PHP',
        'Программист C++', 'Программист C#',
        'Программист C', 'Программист Swift'
        ]
    hh_salary_statistics = get_average_hh_salaries(positions)
    sj_secret_key = os.getenv('SJ_TOKEN')
    sj_salary_statistics = get_average_sj_salaries(positions, sj_secret_key)
    print_vacancies = print_tables(sj_salary_statistics, 'Superjob')
    print_vacancies = print_tables(hh_salary_statistics, 'HeadHunter')


if __name__ == '__main__':
    main()
