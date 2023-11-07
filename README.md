# Rewritings-Analyser
## Подход 2: Поиск рерайтингов при помощи синсетов(наборов синонимов)      

Данный алгоритм реализован Красновым Владиславом. В реализации используются файлы [`synsets.py`], [`synsets-rewritings.json`], [`sample.json`] и база данных [WikiWordnet](https://wiki-ru-wordnet.readthedocs.io/en/latest/)

#### Рассмотрим реализацию подробнее:
Открытие файла, запись файла, метод main, и другие методы можно подробнее рассмотреть в подходе 1, поэтому рассмотрим только реализацию поиска рерайтингов при помощи синсетов.


1. Мы используем базу данных  
2. Посмотрим на функцию `convert_json_into_comparing_dictionary`:
```python
def convert_json_into_comparing_dictionary(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_dictionary = {}
        for item in data:
            shorten_listed_text = delete_short_words_and_punctuation(item["text"])
            data_dictionary[item["id"]] = shorten_listed_text
        return data_dictionary
```
