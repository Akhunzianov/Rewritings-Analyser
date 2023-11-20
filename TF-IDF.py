from LevenshteinDistance import convert_json_into_comparing_dictionary, unpack_json, \
    create_rewritings_file
import math
from collections import Counter
import json
import re


def tf_computation(words):
    word_count = Counter(words)
    total_words = len(words)
    tf = {word: count / total_words for word, count in word_count.items()}
    return tf


def idf_computation(corpus):
    total_documents = len(corpus)
    idf = {}
    for document in corpus:
        words = set(document.split())
        for word in words:
            idf[word] = idf.get(word, 0) + 1

    idf = {word: math.log(total_documents / (count + 1)) for word, count in idf.items()}
    return idf


def tfidf_computation(tf, idf):
    tfidf = {word: tf[word] * idf[word] for word in tf.keys()}
    return tfidf


def euclidean_distance(vec1, vec2):
    common_words = set(vec1) & set(vec2)
    if len(common_words) == 0 or len(common_words) < (len(vec2) * 0.75) or len(common_words) < (len(vec1) * 0.75):
        return 10 ** 9
    distance = math.sqrt(sum((vec1.get(word, 0) - vec2.get(word, 0)) ** 2 for word in common_words))
    return distance


def is_it_rewriting_tfidf(first_tfidf, second_tfidf):
    if euclidean_distance(first_tfidf, second_tfidf) <= 1:
        return True
    return False


def find_tfidf_rewritings(data_dictionary, idf_dictionary):
    length_data = len(data_dictionary)
    for i in range(1, length_data + 1):
        data_dictionary[i][1] = tfidf_computation(data_dictionary[i][1], idf_dictionary)
    rewriting_dictionary = {i: [] for i in range(1, length_data + 1)}
    for h in range(2, length_data + 1):
        first_tfidf = data_dictionary[h][1]
        for j in range(h + 1, length_data + 1):
            second_tfidf = data_dictionary[j][1]
            if is_it_rewriting_tfidf(first_tfidf, second_tfidf):
                rewriting_dictionary[h] += [j]
    return rewriting_dictionary


def dictionary_add_tf(data_dictionary):
    length_data = len(data_dictionary)
    for i in range(1, length_data + 1):
        data_dictionary[i] = [data_dictionary.get(i, 0), tf_computation(data_dictionary[i])]


def unpack_json_text_only(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_dictionary = [re.sub(r'[?,.!:;\"\'1234567890-]', '', item["text"]).lower() for item in data]
        return data_dictionary


def main():
    file = "sample.json"
    data_dictionary = convert_json_into_comparing_dictionary(file)
    dictionary_add_tf(data_dictionary)
    idf_dictionary = idf_computation(unpack_json_text_only(file))
    rewriting_dictionary = find_tfidf_rewritings(data_dictionary, idf_dictionary)
    full_data_dictionary = unpack_json(file)
    create_rewritings_file(rewriting_dictionary, full_data_dictionary, 'tf')


if __name__ == "__main__":
    main()