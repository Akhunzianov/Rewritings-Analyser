from LevenshteinDistance import convert_json_into_comparing_dictionary, unpack_json, \
    create_rewritings_file


def jaccard_index(word1: str, word2: str):
    set_w1 = set(word1)
    set_w2 = set(word2)
    shared = set_w1.intersection(set_w2)
    total = set_w1.union(set_w2)
    jaccard_ind = len(shared) / len(total)
    return jaccard_ind


def is_it_rewriting(first_listed_text_sample, second_listed_text_sample):
    first_listed_text_sample_length = len(first_listed_text_sample)
    second_listed_text_sample_length = len(second_listed_text_sample)
    rewrote_words_cnt = 0
    percentage_for_word_to_be_rewriting = 75  # можно менять процентовку
    percentage_for_text_to_be_rewriting = 75
    for i in range(first_listed_text_sample_length):
        max_index = -1
        for j in range(second_listed_text_sample_length):
            cur_jaccard_index = jaccard_index(first_listed_text_sample[i], second_listed_text_sample[j])
            if cur_jaccard_index > max_index:
                max_index = cur_jaccard_index
        if max_index * 100 > percentage_for_word_to_be_rewriting:
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


def main():
    file = "sample.json"
    data_dictionary = convert_json_into_comparing_dictionary(file)
    rewriting_dictionary = find_rewriting(data_dictionary)
    full_data_dictionary = unpack_json(file)
    create_rewritings_file(rewriting_dictionary, full_data_dictionary, mode='ji')


if __name__ == "__main__":
    main()
