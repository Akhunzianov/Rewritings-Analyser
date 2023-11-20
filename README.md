# Rewritings-Analyser
## Подход 2: Поиск рерайтингов при помощи синсетов(наборов синонимов)      

Данный алгоритм реализован Красновым Владиславом. В реализации используются файлы `synsets.py`, `synsets-rewritings.json`, `sample.json`, морфологический анализатор [pymorphy2](https://pymorphy2.readthedocs.io/en/stable/) и база данных [WikiWordnet](https://wiki-ru-wordnet.readthedocs.io/en/latest/)

#### Рассмотрим реализацию подробнее:
Открытие файла, запись файла, метод main, и другие методы можно подробнее рассмотреть в подходе 1, поэтому рассмотрим только реализацию поиска рерайтингов при помощи синсетов.


1. Посмотрим на функцию `normal_form`:
```python
def normal_form(word):
    word_info = morph.parse(word)[0]
    return word_info.normal_form
```
Эта функция получает на вход слово и возвращает начальную форму этого слова, то есть слово 'арбузы' или 'арбузом' превращается в 'арбуз', таким образом синонимы слова можно легко найти в базе данных или сравнить слово с синонимами.

2. Теперь рассмотрим функцию `find_synonyms`:
```python
def find_synonyms(word):
    word_info = morph.parse(word)[0]
    normal_form = word_info.normal_form
    synonyms = [word_info.word]
    synsets = wikiwordnet.get_synsets(normal_form)
    for i in range(len(synsets)):
        x = synsets[i]
        for w in x.get_words():
            synonyms.append(w.lemma())
    return synonyms
```
Данная функция получает на вход слово, а возвращает список всевозможных синсетов данного слова, то есть возвращает все синонимы слова, даже если у слова несколько смыслов, а также возвращает синонимы в виде трех частей речи, то есть возвращает существительные, прилагательные и глаголы, которые могут считаться синонимом данного слова.(Само слово также находится в списке)

3. Рассмотрим функцию `is_it_rewriting2`:
```python
def is_it_rewriting2(first_listed_text_sample, second_listed_text_sample):
    percentage_of_synsets_to_be_rewriting = 70
    first_listed_text_sample_length = len(first_listed_text_sample)
    second_listed_text_sample_length = len(second_listed_text_sample)
    synsets = []
    cnt_synsets = 0
    for i in range(first_listed_text_sample_length):
        synsets.append(find_synonyms(first_listed_text_sample[i]))
    synonyms = [element for row in synsets for element in row]
    for j in range(second_listed_text_sample_length):
        if normal_form(second_listed_text_sample[j]) in synonyms:
            cnt_synsets += 1
    if (cnt_synsets / max(first_listed_text_sample_length, second_listed_text_sample_length)) > \
            percentage_of_synsets_to_be_rewriting / 100:
        return True
    else:
        return False
```
Данная функция принимает на вход списки слов длины хотя бы 3 двух текстов и определяет являются ли они ререайтингом.
Для этого мы сначала задаём критерий того, что предложение является ререайтингом, записывая в переменную `percentage_of_synsets_to_be_rewriting` процент совпадения, которого достаточно для того, чтобы назвать текст рерайтиногм. Далее с помощью циклов for мы для каждого слова из первого текста создаем список синонимов, который затем объединяем в один список всех синонимов первого текста. Затем мы ищем каждое слово второго текста в списке синонимов и если находим, то увеличиваем переменную `cnt_synsets` на 1. Когда такая операция проделана для всех слов, находим процент рерайтингов от количества слов в наиболее длинном тексе. Если этот процент не меньше `percentage_for_text_to_be_rewriting`, то считаем предложение рерайтингом и возвращаем `True`, иначе `False`.

Данные методы работают вместе с функциями из первого подохода, тем самым повышая точность работы алгоритма.


###### Достоинства подхода:
* Быстрая скорость работы O(n2m2) где n – количество текстов в датасете, m – cреднее количество слов длины не менее 3 в одном тексте.
* Алгоритм довольно точно работает для рерайтингов, в которых используются перестановка слов, удаление слов, использование параллельных конструкций, изменение прямой речи на косвенную.

###### Недостатки подхода:
• Алгоритм не учитывает использование синонимов для рерайтинга и для текстов, в которых этот приём используется часто выдаёт неточные результаты
* Не очень точечно работает для текстов с маленьким количеством слов длины хотя бы 3. Это можно исправить, не удаляя «короткие» слова, но в этом случае увеличивается время работы и может теряться точность в иных случаях.

