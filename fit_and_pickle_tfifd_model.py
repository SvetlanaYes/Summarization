from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pickle
import utils as u

'''
Discription:
This code fits TF-IDF vectorizer with 777572 train files and pickles model

Arguments:
argv[1] - file with train filenames
argv[2] - file to pickle model
'''


def fit_tf_idf_vectorizer(fit_vectorizer_path, train_filenames):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(train_filenames)
    pickle.dump(vectorizer, open(fit_vectorizer_path, 'wb'))


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[train filenames] [file to pickle model] \n")
    train_filenames = u.get_filenames(sys.argv[1])
    fit_vectorizer_path = sys.argv[2]
    fit_tf_idf_vectorizer(fit_vectorizer_path, train_filenames)


if __name__ == "__main__":
    main()
