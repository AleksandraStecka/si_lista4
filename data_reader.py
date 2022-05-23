import io
import json
from copy import deepcopy


# TODO zapis danych do pliku csv po calym procesie preprocessingu
def import_into_csv():
    raw_data = read_file()
    print("No of books in source file: " + str(len(raw_data)))
    initial_cleanup = []
    # usuwane zostaje 9 rekordow z \ ktory nie poprzedza znaku zakodowanego jako utf-16
    for index in range(len(raw_data)):
        try:
            initial_cleanup.append(utf_16_to_utf_8_conversion(raw_data[index]))
        except ValueError:
            pass
    print("No of books after initial cleanup: " + str(len(initial_cleanup)))
    temp_dict = insert_data_into_dict(initial_cleanup)
    print("No of books without missing data: " + str(len(temp_dict.keys())))
    temp_dict = remove_specific_and_broad_genres(temp_dict)
    print("No of books after removing too broad and too specific genres: " + str(len(temp_dict.keys())))
    # lista gatunkow
    counts = count_genres(temp_dict)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Genre list with counts: ")
    for item in sorted_counts:
        print("\t" + item[0] + " " + str(item[1]))


# czytanie surowych danych z pliku zrodlowego
def read_file() -> list[str]:
    with io.open('booksummaries/booksummaries.txt', 'r', encoding='utf-8') as file:
        return file.readlines()


# https://reddit.fun/1604/how-print-strings-with-unicode-escape-characters-correctly?fbclid=IwAR2pX93Wcdntba-4u_BNcEmeD8YREvEaK5Peqtw0h9vN8nkvM6qw_WJUNdQ
# konwersja encodingu utf-16 do utf-8
# rzuca wyjatek ValueError exception - w pliku zrodlowym sa \ ktore nie poprzedzaja znakow utf-16
def utf_16_to_utf_8_conversion(data: str) -> str:
    data = list(data)
    for index, value in enumerate(data):
        if value == '\\':
            utf = ''.join([data[index + k + 2] for k in range(4)])
            for k in range(5):
                data.pop(index)
            data[index] = str(chr(int(utf, 16)))
    return ''.join(data)


# wstawienie danych do slownika, w ktorym kluczem jest identyfikator z wikipedii, a wartoscia jest slownik
# w zagniezdzonym slowniku sa 3 klucze: title, genres, summary
# identyfikator freebase, autor i data publikacji sa pomijane
def insert_data_into_dict(data: list[str]) -> dict[int, dict[str, list[str]]]:
    temp_dict = {}
    for line in data:
        # kolumny w pliku sa podzielone tabulatorami
        line = line.split("\t")
        # line[0] to identyfikator z wikipedii, line[2] to tytul, line[5] to json gatunkow, line[6] to streszczenie
        # spacje z poczatku i konca elementu sa usuwane
        line_stripped = [line[index].strip() for index in (0, 2, 5, 6)]
        # usuwane zostaja rekordy, w ktorych interesujace wartosci sa puste lub ktore zawieraja podejrzane wartosci
        valid = line_stripped[0] != '' and line_stripped[1] != '' and line_stripped[2] != '' \
            and line_stripped[3] != '' and line_stripped[3] != 'To be added.' and line_stripped[3].count("=") == 0 \
            and line_stripped[3].count("\\") == 0 and line_stripped[3].count("/") == 0 \
            and line_stripped[3].count("<") == 0 and line_stripped[3].count("&ndash;") == 0 \
            and line_stripped[3].count("&mdash;") == 0 and line_stripped[3].count("&nbsp;") == 0 \
            and line_stripped[3].count("&#") == 0 and line_stripped[3].count("http") == 0
        if valid:
            nested_dict = {'title': [line_stripped[1]],
                           'genres': [genre for genre in json.loads(line_stripped[2]).values()],
                           'summary': [line_stripped[3]]}
            temp_dict[int(line_stripped[0])] = nested_dict
    return temp_dict


# zliczanie wystapien kazdego z gatunkow
def count_genres(temp_dict: dict[int, dict[str, list[str]]]) -> dict[str, int]:
    counts = {}
    for book in temp_dict.values():
        for genre in book['genres']:
            if genre in counts:
                counts[genre] += 1
            else:
                counts[genre] = 1
    return counts


# usuniecie gatunkow, ktore sa zbyt szerokie lub zbyt waskie
def remove_specific_and_broad_genres(temp_dict: dict[int, dict[str, list[str]]]) -> dict[int, dict[str, list[str]]]:
    counts = count_genres(temp_dict)
    for book in temp_dict.values():
        for genre in deepcopy(book['genres']):
            # zbyt waskie gatunki maja mniej niz 500 wystapien, zbyt szerokie wiecej niz 3000
            if counts[genre] < 500 or counts[genre] > 3000:
                book['genres'].remove(genre)
    helper = deepcopy(temp_dict)
    # usuniecie ksiazek, ktore w wyniku czyszczenia gatunkow nie maja juz przypisanego zadnego gatunku
    for key in helper:
        if len(temp_dict[key]['genres']) == 0:
            temp_dict.pop(key)
    return temp_dict
