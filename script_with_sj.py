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


def predict_rub_hh_salary(hh_url, payload, pages_mumber):
    vacancy_info = {}
    vacancies_processed = 0
    pages_average_salary = []
    for number in range(pages_mumber):
        payload['page'] = number
        response = requests.get(hh_url, params=payload)
        response.raise_for_status()
        for salary in response.json()['items']:
          if salary['salary']['currency'] == 'RUR':
            if salary['salary'] is None:
              pass
            elif salary['salary']['from'] and salary['salary']['to']:
              vacancies_processed += 1
              average_salary = (int(salary['salary']['from'])+int(salary['salary']['to']))/2
              vacancy_info['average_salary'] = int(average_salary)
            elif salary['salary']['from'] is not None:
              vacancies_processed += 1
              average_salary = int(salary['salary']['from'])*1.2
              vacancy_info['average_salary'] = int(average_salary)
            elif salary['salary']['to'] is not None:
              vacancies_processed += 1
              average_salary = int(salary['salary']['to'])*0.8
              vacancy_info['average_salary'] = int(average_salary)
            print(average_salary)
            pages_average_salary.append(average_salary)
    average_salary = count_salary_for_all_pages(pages_average_salary)
    print('страница', average_salary)
    vacancies_found = response.json()['found']
    vacancy_info['vacancies_found'] = vacancies_found
    vacancy_info['vacancies_processed'] = vacancies_processed
    vacancy_info['average_salary'] = int(average_salary)
    return vacancy_info


def predict_rub_sj_salary(sj_url, headers, payload, pages_number):
    vacancy_info = {}
    vacancies_processed = 0
    pages_average_salary = []
    for number in range(pages_number):
        payload['page'] = number
        response = requests.get(sj_url, headers=headers, params=payload)
        response.raise_for_status()
        for salary in response.json()['objects']:
          if salary['currency'] == 'rub':
            salary_from = salary['payment_from']
            salary_to = salary['payment_to']
            if (salary_from is None and salary_to is None) or (salary_from == 0 and salary_to == 0):
              pass
            elif salary_from and salary_to:
              vacancies_processed += 1
              average_salary = (int(salary_to)+int(salary_to))/2
              vacancy_info['average_salary'] = int(average_salary)
            elif salary_from is not None or salary_from == 0:
              vacancies_processed += 1
              average_salary = int(salary_from)*1.2
              vacancy_info['average_salary'] = int(average_salary)
            elif salary_to is not None or salary_to == 0:
              vacancies_processed += 1
              average_salary = int(salary_to)*0.8
              vacancy_info['average_salary'] = int(average_salary)
            print(average_salary)
            pages_average_salary.append(average_salary)
    average_salary = count_salary_for_all_pages(pages_average_salary)
    print('страница', number, average_salary)
    vacancies_found = response.json()['total']
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