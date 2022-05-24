# analiza zbioru danych
def dataset_analysis(dataset: dict[int, dict[str, str]]):
    print("Dataset size: " + str(len(dataset)))
    print()
    counts = count_genres_occurrences(dataset)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Genre list with book counts: ")
    for item in sorted_counts:
        print("\t" + item[0] + " " + str(item[1]))
    print()
    print("Average no of words per summary: " + str(get_avg_word_count(dataset)))
    word_len_occurrences = count_len_words_occurrences(dataset)
    sorted_word_lens = sorted(word_len_occurrences.items(), key=lambda x: x[1], reverse=True)
    print("Most common no of words in summary: " + str(sorted_word_lens[0][0]))
    sorted_word_lens = sorted(word_len_occurrences.items(), key=lambda x: x[0], reverse=True)
    print("Max no of words in summary: " + str(sorted_word_lens[0][0]))
    print("Min no of words in summary: " + str(sorted_word_lens[len(sorted_word_lens) - 1][0]))
    print()
    print("Average no of characters per summary: " + str(get_avg_char_count(dataset)))
    char_len_occurrences = count_len_chars_occurrences(dataset)
    sorted_char_lens = sorted(char_len_occurrences.items(), key=lambda x: x[1], reverse=True)
    print("Most common no of characters in summary: " + str(sorted_char_lens[0][0]))
    sorted_char_lens = sorted(char_len_occurrences.items(), key=lambda x: x[0], reverse=True)
    print("Max no of characters in summary: " + str(sorted_char_lens[0][0]))
    print("Min no of characters in summary: " + str(sorted_char_lens[len(sorted_char_lens) - 1][0]))
    print()
    counts = count_words_occurrences(dataset)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("10 most common words: ")
    for index in range(10):
        print("\t" + sorted_counts[index][0] + " " + str(sorted_counts[index][1]))


# zliczanie wystapien kazdego z gatunkow
def count_genres_occurrences(dataset: dict[int, dict[str, str]]) -> dict[str, int]:
    counts = {}
    for book in dataset.values():
        if book['genre'] in counts:
            counts[book['genre']] += 1
        else:
            counts[book['genre']] = 1
    return counts


# srednia dlugosc streszczenia w liczbie slow
def get_avg_word_count(dataset: dict[int, dict[str, str]]) -> float:
    count = 0
    for book in dataset.values():
        words = book['summary'].split()
        # zliczane sa tylko teksty, ktore sa slowami
        for word in words:
            if is_word(word):
                count += 1
    return round(count / len(dataset), 3)


# srednia dlugosc streszczenia w liczbie znakow
def get_avg_char_count(dataset: dict[int, dict[str, str]]) -> float:
    count = 0
    for book in dataset.values():
        count += len(book['summary'])
    return round(count / len(dataset), 3)


# najczestsza dlugosc streszczenia w liczbie slow
def count_len_words_occurrences(dataset: dict[int, dict[str, str]]) -> dict[int, int]:
    temp_dict = {}
    for book in dataset.values():
        count = 0
        words = book['summary'].split()
        for word in words:
            if is_word(word):
                count += 1
        if count in temp_dict:
            temp_dict[count] += 1
        else:
            temp_dict[count] = 1
    return temp_dict


# najczestsza dlugosc streszczenia w liczbie znakow
def count_len_chars_occurrences(dataset: dict[int, dict[str, str]]) -> dict[int, int]:
    temp_dict = {}
    for book in dataset.values():
        count = len(book['summary'])
        if count in temp_dict:
            temp_dict[count] += 1
        else:
            temp_dict[count] = 1
    return temp_dict


# zliczanie wystapien kazdego slowa
def count_words_occurrences(dataset: dict[int, dict[str, str]]) -> dict[str, int]:
    counts = {}
    for book in dataset.values():
        words = book['summary'].split()
        for word in words:
            word = word.lower()
            if word in counts:
                counts[word] += 1
            elif is_word(word):
                counts[word] = 1
    return counts


# sprawdzenie czy tekst jest faktycznie slowem
def is_word(string: str) -> bool:
    for i in range(len(string)):
        if (string[i].lower() < "a" or string[i].lower() > "z") and string[i] != "'":
            return False
    return True
