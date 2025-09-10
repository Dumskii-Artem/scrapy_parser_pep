# Проект 20-го спринта Python YandexPracticum 


Парсер [официального списка PEP](https://peps.python.org/) — Python Enhancement Proposals.  
Собирает таблицу всех PEP с номерами, названиями и статусами, а также формирует CSV-отчёт по статусам.

---

## Технологии

- Python 3.9+
- Scrapy 2.x

---

## Установка

```bash
git clone https://github.com/Dumskii-Artem/scrapy_parser_pep.git
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# или
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

## Запуск

```bash
scrapy crawl pep
```

## Результаты
После запуска появятся два CSV-файла в директории results/:

pep_<datatime>.csv — таблица всех PEP
number,name,status

status_summary_<datatime>.csv — статистика по статусам
Статус, Количество

запуск тестов 
```
pytest
```

## Автор проекта
[Думский Артём](https://github.com/Dumskii-Artem) в рамках обучения
на Яндекс.Практикум по программе Python-разработчик расширенный (когорта 57+)
