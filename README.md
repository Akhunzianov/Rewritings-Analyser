# Rewritings-Analyser
В данном репизитории реализованы 3 метода выявления рерайтинга алгоритмическими методами.

## Подход 1: Расстояние Левенштейна
Данный алгоритм реализован Ахунзяновым Ренатом. В реализации используются файлы [`LevenshteinDistance.py`](https://github.com/Akhunzianov/Rewritings-Analyser/blob/2f4faad08bca08cec0d6d5a58ff7d95ccf28e739/LevenshteinDistance.py), [`sample.json`](https://github.com/Akhunzianov/Rewritings-Analyser/blob/2f4faad08bca08cec0d6d5a58ff7d95ccf28e739/sample.json), [`rewritings_levenshtein.json`](https://github.com/Akhunzianov/Rewritings-Analyser/blob/2f4faad08bca08cec0d6d5a58ff7d95ccf28e739/rewritings_levenshtein_distance.json)

Результат работы данного метода записан в файле [`rewritings_levenshtein.json`](https://github.com/Akhunzianov/Rewritings-Analyser/blob/2f4faad08bca08cec0d6d5a58ff7d95ccf28e739/rewritings_levenshtein_distance.json)

#### Рассмотрим реализацию подробнее:

Метод `main` не имеет реализации какого-либо процесса, а просто поочередно вызывает функции, реализующие алгоритм 
```python
  def main():
    file = "sample.json"
    data_dictionary = convert_json_into_comparing_dictionary(file)
    rewriting_dictionary = find_rewriting(data_dictionary)
    full_data_dictionary = unpack_json(file)
    create_rewritings_file(rewriting_dictionary, full_data_dictionary)
```
###### Рассмотри методы вызываемые в `main` по очередности:

1. Посмотрим на функцию `convert_json_into_comparing_dictionary`:
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
Данная функция открывает файл с данными, создаёт пустой словарь `data_dictionary`, затем проходит по всем текстам в предложенном файле и записывает в словарь пары  ключ-значение, где ключ - это id текста, а значение - это текст, обработанный функцией `delete_short_words_and_punctuation`, рассмотрим работу этой функции:
```python
def delete_short_words_and_punctuation(text_sample):
    no_punctuation_text = re.sub(r'[?,.!:;\"\'1234567890-]', '', text_sample)
    text_list = no_punctuation_text.split()
    for i in range(len(text_list) - 1, -1, -1):
        if len(text_list[i]) <= 2:  # можно менять резмер коротких слов
            del text_list[i]
    return text_list
```
Данная функция сначала заменяет все знаки препинания и цыфры в сторке на пустую строку, затем делит текст на список слов и удаляет из этого списка все слова короче 3 букв. Затем функция возвращает получившийся список.

Таким образом функция `convert_json_into_comparing_dictionary` записывает в значения словаря список длины не менее 3 слов текста и возвращает полученный таким образом словарь, который записывается в переменную `data_dictionary` в методе `main`
 
2. Теперь рассотрим функцию `find_rewriting`:
```python
def find_rewriting(data_dictionary):
    length_data = len(data_dictionary)
    rewriting_dictionary = {i: [] for i in range(1, length_data + 1)}
    for i in range(1, length_data + 1):
        first_listed_text_sample = data_dictionary[i]
        for j in range(i + 1, length_data + 1):
            second_listed_text_sample = data_dictionary[j]
            if is_it_rewriting(first_listed_text_sample, second_listed_text_sample):
                rewriting_dictionary[i] += [j]
    return rewriting_dictionary
```
Данная функция принимает на вход словарь, полученный на предыдущем шаге, затем записывает его длинну в переменную `length_data`, создаёт словарь, ключами которого являются все id наших текстов (то есть числа от 1 до длинны датасета). Далее циклом for мы проходим по всем id наших текстов и записываем в переменную `first_listed_text_sample` список слов длины не менее 3 текста с id равным i. Далее мы проходим по всем текстам, у которых id больше id текста `first_listed_text_sample`. Мы идём не по всем текстам для экономии времени, т.е. для избежания ситуации, когда какие-то два текста сравниваются несколько раз. Затем мы вызываем фцнкцию `is_it_rewriting` для определения, являются ли предложения реерайтингом.
```python
def is_it_rewriting(first_listed_text_sample, second_listed_text_sample):
    first_listed_text_sample_length = len(first_listed_text_sample)
    second_listed_text_sample_length = len(second_listed_text_sample)
    rewrote_words_cnt = 0
    percentage_for_word_to_be_rewriting = 60  # можно менять процентовку
    percentage_for_text_to_be_rewriting = 75
    for i in range(first_listed_text_sample_length):
        min_distance = 10 ** 9
        for j in range(second_listed_text_sample_length):
            editing_distance = levenshtein_distance(first_listed_text_sample[i], second_listed_text_sample[j])
            if editing_distance < min_distance:
                min_distance = editing_distance
        if min_distance / len(first_listed_text_sample[i]) * 100 <= 100 - percentage_for_word_to_be_rewriting:
            rewrote_words_cnt += 1
    if rewrote_words_cnt / max(first_listed_text_sample_length,
                               second_listed_text_sample_length) * 100 >= percentage_for_text_to_be_rewriting:
        return True
    return False
```
Данная функция принимает на вход списки слов длины хотя бы 3 двух текстов и определяет являются ли они ререайтингом.
Для этого мы сначала задаём критерии того, что слово являестя рерайтингом и, что предложение является ререайтингом, записывая в переменные `percentage_for_word_to_be_rewriting` и `percentage_for_text_to_be_rewriting` процент совпадения, которого достаточно для того, чтобы назвать слово/текст рерайтиногм. Далее с помощью циклов for мы для каждого слова из первого текста проверяем слова из второго текста на рерайтинг. Для этого мы находим для каждого слова первого предложения слово из второго предложения с минимальным расстоянием Левенштейна, далее если процент правок для получения из первого слова второго по отношению к длине первого слова не превосходит `100 - percentage_for_word_to_be_rewriting`, то считаем слово рерайтингом и прибавляем к счётчику слов-рерайтингов `rewrote_words_cnt` 1. Когда такая операция проделана для всех слов, находим процент рерайтингов от количества слов в наиболее длинном тексе. Если этот процент не меньше `percentage_for_text_to_be_rewriting`, то считаем предложение рерайтингом и возвращаем `True`, иначе `False`

Ремарка по поводу реализации алгоритма поиска расстоянил Левенштейна:

Данный алгорит реализован 2 функциями
```python
def substitute_difference(letter1, letter2):
    return letter1 != letter2


def levenshtein_distance(word1, word2):
    if len(word2) < len(word1):
        word1, word2 = word2, word1
    previous = [z for z in range(len(word1) + 1)]
    current = []
    for i in range(1, len(word2) + 1):
        for j in range(len(word1) + 1):
            if j == 0:
                current.append(i)
            else:
                insertation = current[j - 1] + 1
                delete = previous[j] + 1
                substitute = previous[j - 1] + substitute_difference(word1[j - 1], word2[i - 1])
                current.append(min(insertation, delete, substitute))
        previous, current = current, []
    return previous[-1]
```
Реализован алгоритм итеративным подходом с минимальными затратами по памяти. Мы храним только 2 массива: `previous` и `current`. Алгоритм расчитывает очередное значения для массива `current`, как мининмум из `insertation = current[j - 1] + 1`, `delete = previous[j] + 1`, `substitute = previous[j - 1] + substitute_difference(word1[j - 1], word2[i - 1])`, то есть выбирая наболее благоприятный случай из удаления элемента из сторки, вставкой элемента в строку и заменой элемента на другой. В данном случае функция `substitute_difference` не несёт большой смысловой нагрузки и только отвечает на вопрос, равны ли элементы, но в перспективе данную функцию можно сделать сложнее, добавив разные веса замене разных букв. Таким образом мы реализуем алгоритм вычисления рассотяния Левенштейна, находя его для префиксов исходных слов и итеративно доходя до полных слов, при этом не храня в памяти всю матрицу сравнения для всех префиксов, а лишь последние её 2 строки.
Также можно заметить, что возможно назначить разным операциям (вставка, удаление, замена) разные веса для более точных результатов.

Теперь мы выяснили, являются ли данные два текста рерайтингом. Тогда вернёмся к функции `find_rewriting`. Если мы поняли, что очередные два текста являются рерайтингом, то в словарь `rewriting_dictionary` по ключу равному id первого такста добавляется значение, равное id второго текста. И после прохода по всем парам предложений функция возвращает словарь `rewriting_dictionary`. 
Заметим, что если у нас есть два предложения с id равными n и m где n<=m, то в полученном словаре в списке значений ключа n будет находиться m, однако в списке значений ключа m не будет n. Это не ошибка, так происходит именно потому, что каждая пара текстов сравнивается только однажды, а также это уменьшает затраты по памяти и упрощает запись результатов в файл.

3. Рассмотри функцию `unpack_json`:
```python
def unpack_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_dictionary = {}
        for item in data:
            data_dictionary[item["id"]] = item["text"]
        return data_dictionary
```
Данная функция принимает на вход название исходного файли и возвращает словарь, в котором ключи - это id текстов, а значения - сами тексты. Заметим, что данный функционал можно производить при первом считываниии файла, однако в ходе поиска рерайтингов он не нужен (нужен словарь с списками слов без знаков преринания и коротких слов), поэтому для того, чтобы он не нагружал памать во время алогритма, мы делаем повторное открытие файла. 

4. Посмотрим на `create_rewritings_file`:
```python
def create_rewritings_file(rewriting_dictionary, full_data_dictionary):
    data = []
    length = len(rewriting_dictionary)
    used_text_samples_ids = set()
    for i in range(1, length + 1):
        current_set = []
        if i not in used_text_samples_ids and len(rewriting_dictionary[i]) != 0:
            current_set.append({"id": i, "text": full_data_dictionary[i]})
            used_text_samples_ids.add(i)
            for el in rewriting_dictionary[i]:
                current_set.append({"id": el, "text": full_data_dictionary[el]})
                used_text_samples_ids.add(el)
            data.append(current_set)

    with open("rewritings_levenshtein_distance.json", "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
```
Данный метод проходит по словарю `rewriting_dictionary` и при условии, что список рерайтингов для данного текста не пуст, добавляет словарь со значениями id и text для каждого рерайтинги и самого текста в список `current_set`, а id рерайтингов и самого текста в множество `used_text_samples_ids` (это делается, чтобы в файл болки с рерайтингами не записывались по несколько раз), а затем список `current_set` добавляется в массив `data`, который в после конца цикла представляет собой массив, который включает в себя списки рерайтингов, объединённые в массивы. Этот список и записывается в файл `rewritings_levenshtein.json`.

###### Достоинства подхода:
* Сравнительно небольшое время работы. Алгоритм работает за время _O(n<sup>2</sup>m<sup>2</sup>l<sup>2</sup>)_, где _n_ – количество текстов в датасете, _m_ – cреднее количество слов длинны не менее 3 в одном тексте, _l_ – среднее количество букв в слове длинны хотя бы 3 в датасете
* Алгоритм точно работает для рерайтингов, в которых используются перестановка слов, удаление слов, использование параллельных конструкций, изменение прямой речи на косвенную
* Есть возможность добавить веса для разных операций (замена, удаление, вставка) в алгоритм нахождения расстояния Левенштейна для более точных сравнений
###### Недостатки подхода:
* Алгоритм не учитывает использование синонимов для рерайтинга и для текстов, в которых этот приём используется часто выдаёт неточные результаты
* Не очень точено работает для текстов с маленьким количеством слов длины хотя бы 3. Это можно исправить, не удаляя «короткие» слова, но в этом случае увеличивается время работы и может теряться точность в иных случаях.
