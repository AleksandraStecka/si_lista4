# analiza zbioru danych
def dataset_analysis(dataset: dict[int, dict[str, str]]):
    print("Dataset size: " + str(len(dataset)))
    counts = count_genres(dataset)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Genre list with book counts: ")
    for item in sorted_counts:
        print("\t" + item[0] + " " + str(item[1]))


# zliczanie wystapien kazdego z gatunkow
def count_genres(dataset: dict[int, dict[str, str]]) -> dict[str, int]:
    counts = {}
    for book in dataset.values():
        if book['genre'] in counts:
            counts[book['genre']] += 1
        else:
            counts[book['genre']] = 1
    return counts
