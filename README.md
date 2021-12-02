## Сравниваем вакансии программистов

Данный скрипт позволит узнать усредненную зарплату разработчиков ПО для разных языков программирования.
Информация взята из публичного доступа на сайтах [HeadHunter](HH.ruhttps://hh.ru) и [Superjob](https://superjob.ru).

## Как установить

- Скачай программу себе на компьютер.
- Получите ключ к [API Superjob](https://api.superjob.ru).
- Создай файл .env и укажи секретный ключ Superjob.
```buildoutcfg
SJ_TOKEN='Тут секретный ключ'
```
- Создай [виртуальное окружение](https://python-scripts.com/virtualenv) для проекта.
- Установи зависимости.
```bash
pip install -r requirements.txt
```
- Запусти скрипт.
```bash
python developers_salaries.py
```
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков Devman](https://dvmn.org).
Прочитать [английскую версию](https://github.com/Staskosh/Avarage_developers_salaries/blob/main/README_ENG.md)