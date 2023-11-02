import json
import re


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


def delete_short_words_and_punctuation(text_sample):
    no_punctuation_text = re.sub(r'[?,.!:;\"\'1234567890-]', '', text_sample)
    text_list = no_punctuation_text.split()
    for i in range(len(text_list) - 1, -1, -1):
        if len(text_list[i]) <= 2:  # можно менять резмер коротких слов
            del text_list[i]
    return text_list


def convert_json_into_comparing_dictionary(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_dictionary = {}
        for item in data:
            shorten_listed_text = delete_short_words_and_punctuation(item["text"])
            data_dictionary[item["id"]] = shorten_listed_text
        return data_dictionary


def unpack_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_dictionary = {}
        for item in data:
            data_dictionary[item["id"]] = item["text"]
        return data_dictionary


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

    with open("rewritings.json", "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def main():
    file = "sample.json"
    data_dictionary = convert_json_into_comparing_dictionary(file)
    rewriting_dictionary = find_rewriting(data_dictionary)
    full_data_dictionary = unpack_json(file)
    create_rewritings_file(rewriting_dictionary, full_data_dictionary)


if __name__ == "__main__":
    main()