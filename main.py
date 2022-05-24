from data_reader import process_and_import_into_csv
from data_reader import read_from_csv
from data_analyser import dataset_analysis


if __name__ == '__main__':
    # process_and_import_into_csv()
    dataset = read_from_csv()
    dataset_analysis(dataset)
