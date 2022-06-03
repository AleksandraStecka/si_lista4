import numpy
import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


class Colors:
    GREEN = '\u001b[92m'
    END = '\033[0m'


def multinomial_naive_bayes():
    multinomial_naive_bayes_reg()
    multinomial_naive_bayes_cross_val()


def multinomial_naive_bayes_reg():
    dataset = pandas.read_csv('booksummaries/processed_data.csv', names=['id', 'genre', 'summary'])
    # podzial zbioru danych na zbior trenujacy (90%) i testujacy / walidujacy (10%)
    x_train, x_validate, y_train, y_validate = train_test_split(dataset['summary'], dataset['genre'], train_size=0.9)
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    # CountVectorizer zamienia tablice dokumentow na macierz liczby wystapien tokenow (cech)
    # max_df, min_df - gorna i dolna granicza ignorowania slow o zbyt czestym lub zbyt rzadkim wystepowaniu
    # max_features - maksymalna liczba wyznaczonych cech
    # ngram_range - liczba slow ktora moze byc traktowana jako cecha
    count_vectorizer = CountVectorizer(max_df=0.8, min_df=0.01, max_features=5000, ngram_range=(1, 2))
    x_train_counts = count_vectorizer.fit_transform(x_train)
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
    # TfidfTransformer zamienia macierz liczby wystapien na znormalizowana reprezentacje tf lub tf-idf
    # tf = czestosc wystepowania slowa w dokumencie
    # tf-idf = czestosc wystepowania slowa w dokumencie w stosunku do rozmiaru dokumentu
    # korzystam z tf-idf bo streszczenia fabuly maja rozna dlugosc
    tfidf_transformer = TfidfTransformer(use_idf=True)
    x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
    # utworzenie i wyuczenie modelu uczenia maszynowego
    # model jest uczony na odpowiednio przygotowanym zbiorze danych wejsciowych i zbioru wyjsc dla kazdego wejscia
    ml_model = MultinomialNB(alpha=0.01)
    ml_model.fit(x_train_tfidf, y_train)
    # model wyznacza zbior gatunkow dla zbioru streszczen na podstawie tego czego sie nauczyl
    y_pred = ml_model.predict(count_vectorizer.transform(x_validate))
    print("Prediction accuracy mean: ", end="")
    print(round(numpy.mean(y_pred == y_validate), 3))
    print()
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html
    # precision = zdolnosc modelu do nie przypisywania do streszczenia gatunku, jezeli ksiazka nie jest tego gatunku
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html
    # recall = zdolnosc modelu do znalezienia wszystkich streszczen ksiazek danego gatunku
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
    # f1-score = srednia harmoniczna z precision i recall, gdzie 1 to najlepsza wartosc, a 0 najgorsza
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
    # support = liczba wystapien kazdego z gatunkow w y_validate
    print("Classification report:")
    print(classification_report(y_validate, y_pred))
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # confusion matrix = macierz sluzaca do okreslenia prawdziwosci klasyfikacji
    # wartosc w komorce i,j reprezentuje liczbe streszczen, ktore byly gatunku i, a ktorym przypisano gatunek j
    # z tego powodu na przekatnej powinny byc najwieksze wartosci
    matrix = confusion_matrix(y_validate, y_pred)
    print("Confusion matrix:")
    for i in range(len(matrix)):
        print("\t", end="")
        for j in range(len(matrix[i])):
            if i == j:
                print(f'{Colors.GREEN}{matrix[i][j]:3d}{Colors.END}', end=" ")
            else:
                print(f'{matrix[i][j]:3d}', end=" ")
        print()
    print()


def multinomial_naive_bayes_cross_val():
    dataset = pandas.read_csv('booksummaries/processed_data.csv', names=['id', 'genre', 'summary'])
    # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
    # zgodnie z wymaganiami w liscie zadan dokonywana jest 10-krotna walidacja krzyzowa
    count_vectorizer = CountVectorizer(max_df=0.8, min_df=0.01, max_features=5000, ngram_range=(1, 2))
    x_train_counts_full = count_vectorizer.fit_transform(dataset['summary'])
    tfidf_transformer = TfidfTransformer(use_idf=True)
    x_train_tfidf_full = tfidf_transformer.fit_transform(x_train_counts_full)
    ml_model = MultinomialNB(alpha=0.01)
    cross_validation = cross_validate(ml_model, x_train_tfidf_full, dataset['genre'], cv=10)
    print("Fit times for each iteration:")
    for element in cross_validation['fit_time']:
        print("\t" + str(round(element, 5)))
    print()
    print("Score times for each iteration:")
    for element in cross_validation['score_time']:
        print("\t" + str(round(element, 5)))
    print()
    print("Test scores for each iteration:")
    for element in cross_validation['test_score']:
        print("\t" + str(round(element, 3)))
    print()
    print("Prediction accuracy mean: ", end="")
    print(round(numpy.mean(cross_validation['test_score']), 3))
