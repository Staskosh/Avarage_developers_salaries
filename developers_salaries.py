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


def calculate_sj_salary(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        predicted_salary = predict_salary(salary_from, salary_to)
        return predicted_salary


def get_sj_salaries(sj_secret_key, position):
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    development_and_programing = 48
    moscow = 4
    headers = {
        'X-Api-App-Id': sj_secret_key
    }
    payload = {
        'keyword': position,
        'catalogues': development_and_programing,
        'town': moscow,
    }
    salary_sum = 0
    vacancies_processed = 0
    for page_number in count(0):
        payload['page'] = page_number
        response = requests.get(sj_url, headers=headers, params=payload)
        response.raise_for_status()
        page = response.json()
        vacancies = page['objects']
        for vacancy in vacancies:
            predicted_salary = calculate_sj_salary(vacancy)
            if predicted_salary:
                salary_sum += predicted_salary
                vacancies_processed += 1
        if not page['more']:
            break
    vacancies_found = page['total']
    return salary_sum, vacancies_processed, vacancies_found


def calculate_hh_salary(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        predicted_salary = predict_salary(salary_from, salary_to)
        return predicted_salary


def get_hh_salary(position):
    hh_url = 'https://api.hh.ru/vacancies'
    development_programing = '1.221'
    month = '31'
    moscow = '1'
    payload = {
        'text': position,
        'specialization': development_programing,
        'period': month,
        'area': moscow,
    }
    salary_sum = 0
    vacancies_processed = 0
    for page_number in count(0):
        payload['page'] = page_number
        response = requests.get(hh_url, params=payload)
        response.raise_for_status()
        page = response.json()
        vacancies = page['items']
        total_pages = page['pages']
        for vacancy in vacancies:

            predicted_salary = calculate_hh_salary(vacancy)
            if predicted_salary:
                salary_sum += predicted_salary
                vacancies_processed += 1
        if page_number >= total_pages - 1:
            break
    vacancies_found = page['found']
    return salary_sum, vacancies_processed, vacancies_found


def get_average_hh_salaries(positions):
    vacancies = {}
    for position in positions:
        salary_sum, vacancies_processed, vacancies_found = get_hh_salary(position)
        if vacancies_processed:
            vacancies[position] = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': int(salary_sum / vacancies_processed)
            }
    return vacancies


def get_average_sj_salaries(positions, sj_secret_key):
    vacancies = {}
    for position in positions:
        salary_sum, vacancies_processed, vacancies_found = get_sj_salaries(sj_secret_key, position)
        if vacancies_processed:
            vacancies[position] = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': int(salary_sum / vacancies_processed)
            }
    return vacancies


def create_table(average_salaries, source):
    title = source + ' Moscow'
    table = [
        [
            '???????? ????????????????????????????????',
            '???????????????? ??????????????',
            '???????????????? ????????????????????',
            '?????????????? ????????????????',
        ],
    ]
    for position, statistics in average_salaries.items():
        position_salariy = [
            position,
            statistics['vacancies_found'],
            statistics['vacancies_processed'],
            statistics['average_salary'],
        ]
        table.append(position_salariy)
    table = AsciiTable(table, title)
    return table


def main():
    load_dotenv()
    positions = [
        '?????????????????????? JavaScript', '?????????????????????? Java',
        '?????????????????????? Python', '?????????????????????? PHP',
        '?????????????????????? C++', '?????????????????????? C#',
        '?????????????????????? C', '?????????????????????? Swift'
        ]
    hh_salary_statistics = get_average_hh_salaries(positions)
    sj_secret_key = os.getenv('SJ_TOKEN')
    sj_salary_statistics = get_average_sj_salaries(positions, sj_secret_key)
    print(create_table(sj_salary_statistics, 'Superjob').table)
    print(create_table(hh_salary_statistics, 'HeadHunter').table)


if __name__ == '__main__':
    main()
