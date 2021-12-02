## Programming vacancies compare

This script will allow you to find out the average salary of software developers for different programming languages.
The information is taken from public access on the [HeadHunter](http://hh.ru) and [Superjob](https:superjob.ru).

## How to install

- Download the program to your computer.
- Get the key to [Superjob API](https://api.superjob.ru).
- Create a .env file and specify the Superjob secret key.
```buildoutcfg
SJ_TOKEN='Here's the secret key'
```
- Create a [virtual environment](https://python-scripts.com/virtualenv) for the project.
- Install dependencies.
```bash
pip install -r requirements.txt
```
- Run the script.
```bash
python developers_salaries.py
````

## Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org).
Read the [Russian version](https://github.com/Staskosh/Avarage_developers_salaries/blob/main/README.md).