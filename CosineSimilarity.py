from LevenshteinDistance import convert_json_into_comparing_dictionary, unpack_json, \
    create_rewritings_file
import math
import re
from collections import Counter

WORD = re.compile(r"\w+")


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


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def find_rewriting(data_dictionary):
    length_data = len(data_dictionary)
    rewriting_dictionary = {i: [] for i in range(1, length_data + 1)}
    for i in range(1, length_data + 1):
        first_listed_text_sample = data_dictionary[i]
        for j in range(i + 1, length_data + 1):
            second_listed_text_sample = data_dictionary[j]
            if get_cosine(first_listed_text_sample, second_listed_text_sample):
                rewriting_dictionary[i] += [j]
    return rewriting_dictionary


def main():
    file = "sample.json"
    data_dictionary = convert_json_into_comparing_dictionary(file)
    rewriting_dictionary = find_rewriting(data_dictionary)
    full_data_dictionary = unpack_json(file)
    create_rewritings_file(rewriting_dictionary, full_data_dictionary, mode='ji')


if __name__ == "__main__":
    main()
