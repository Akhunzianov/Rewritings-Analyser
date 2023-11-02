import pymorphy2
from wiki_ru_wordnet import WikiWordnet
wikiwordnet = WikiWordnet()
# Инициализируем анализатор pymorphy2
morph = pymorphy2.MorphAnalyzer()
# Слово, для которого мы хотим найти синонимы
word = "хуй"
# Функция для нахождения синонимов
def find_synonyms(word):
    word_info = morph.parse(word)[0]
    # Извлекаем нормальную форму слова
    normal_form = word_info.normal_form
    synonyms = [word_info.word]
    synsets = wikiwordnet.get_synsets(normal_form)
    for i in range(len(synsets)):
        x = synsets[i]
        for w in x.get_words():
            synonyms.append(w.lemma())
    # Добавляем само слово в список синонимов

    # Здесь вы можете добавить ваш собственный список синонимов на основе тезауруса
    # Например, synonyms.extend(["синоним1", "синоним2"])

    return synonyms

synonyms = find_synonyms(word)
if synonyms:
    print(f"Синонимы слова '{word}': {', '.join(synonyms)}")
else:
    print(f"Не удалось найти синонимы для слова '{word}'")

