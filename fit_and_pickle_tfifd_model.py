# TODO: refactor and improve code
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pickle

'''
Discription:
This code fits TF-IDF vectorizer with 777572 train files and pickles model

Arguments:
argv[1] - file with train filenames
argv[2] - file to pickle model
'''
path = ''
filename = ''
vectorizer = TfidfVectorizer()
folder_names = {
    '1': '/home/lab/Desktop/data/Tokenized/168tokenized/',
    'A': '/home/lab/Desktop/data/Tokenized/aravot_tokenized/',
    'I': '/home/lab/Desktop/data/Tokenized/Infocom_token/',
    'T': '/home/lab/Desktop/data/Tokenized/tokenized/'
}


def get_filenames():
    global path
    with open(path, 'r') as f:
        list_of_names = f.readlines()
    print(len(list_of_names))
    return list_of_names


def fit_tf_idf_vectorizer():
    filenames = get_filenames()
    vectorizer.fit(filenames)
    pickle.dump(vectorizer, open(filename, 'wb'))


def main():
    global path, filename
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[train filenames]")
    path = sys.argv[1]
    filename = sys.argv[2]
    fit_tf_idf_vectorizer()


main()

