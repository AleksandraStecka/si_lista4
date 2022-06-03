from data_reader import process_and_import_into_csv
from data_reader import read_from_csv
from data_analyser import dataset_analysis
from classifiers import *
import pandas


if __name__ == '__main__':
    # process_and_import_into_csv()
    # dataset_to_analyse = read_from_csv()
    # dataset_analysis(dataset_to_analyse)
    # dataset = pandas.read_csv('booksummaries/processed_data.csv', names=['id', 'genre', 'summary'])
    multinomial_naive_bayes()
