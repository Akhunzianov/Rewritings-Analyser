# Rewritings-Analyser
## Подход 4: Поиск рерайтингов при помощи косинусного сходства   

Данный алгоритм реализовал Краснов Владислав. В реализации используются файлы `CosineSimilarity.py`, `sample.json`, `rewritings_cosine_similarity` и билиотеки `math` и `collections`.

#### Рассмотрим реализацию подробнее:
Открытие файла, запись файла, метод main, и другие методы можно подробнее рассмотреть в подходе 1, поэтому рассмотрим только реализацию поиска рерайтингов при помощи косинусного сходства.

1. Посмотрим на функцию `text_to_vector`:
```python
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
```
 Данная функция переводит строку в словарь-вектор, где ключи - сами слова, а значения - количества вхождений данного слова в строку.

2. Теперь рассмотрим функцию `get_cosine`:
```python
   def get_cosine(first_listed_text_sample, second_listed_text_sample):
    percentage_for_text_to_be_rewriting = 0
    first_listed_text_sample = ' '.join(first_listed_text_sample)
    second_listed_text_sample = ' '.join(second_listed_text_sample)
    vec1 = text_to_vector(first_listed_text_sample)
    vec2 = text_to_vector(second_listed_text_sample)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return False
    else:
        percentage_for_text_to_be_rewriting = float(numerator) / denominator
        if percentage_for_text_to_be_rewriting > 0.75:
            return True
        else:
            return False
```
Данная функция считает косинусное сходство при помощи формулы ![image](https://github.com/Akhunzianov/Rewritings-Analyser/assets/76743076/9946a7f5-c6e5-4996-bd60-683ebc19453c). Сначала считаем пересечения, то есть слова, которые есть в обоих предложениях, затем считаем числитель и знаменатель и сравниваем, получается ли сходство > 0.75, если да, то предложения можно считать очень близкими.

###### Достоинства подхода:
• Быстрая скорость работы O(n2m2) где n – количество текстов в датасете, m – cреднее количество слов длины не менее 3 в одном тексте. 

• Алгоритм довольно точно работает для рерайтингов, в которых используются перестановка слов, удаление слов, использование параллельных конструкций, изменение прямой речи на косвенную.

###### Недостатки подхода:
• Алгоритм не учитывает использование синонимов для рерайтинга и для текстов, в которых этот приём используется часто выдаёт неточные результаты

• Не очень точечно работает для текстов с маленьким количеством слов длины хотя бы 3. Это можно исправить, не удаляя «короткие» слова, но в этом случае увеличивается время работы и может теряться точность в иных случаях.


