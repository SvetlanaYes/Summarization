import stanza
import json
import os
from configparser import ConfigParser
import sys
import utils as u

"""
    Args:
         stopwords: Armenian stopwords path
         filenames: File with train/test filenames(json)
    Discription:
    This code lemmatizes texts with stanza.Pipeline, removes stopwords from the texts and adds lemma keys to json files
    
"""


file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)
nlp = stanza.Pipeline('hy', tokenize_pretokenized=True, processors='tokenize,lemma')


def get_lemmas(text, stopwords):
    """

    Args:
        text: original text loaded from json file
        stopwords: Armenian stopwords path

    Returns: list with lemmatized words of text, without stopwords

    """
    lemmatized_no_stopwords_text = []
    processed_text = nlp(text)
    for s in processed_text.sentences:
        for w in s.words:
            if w.lemma not in stopwords:
               lemmatized_no_stopwords_text.append(w.lemma)
    return lemmatized_no_stopwords_text


def add_lemma_key(file_path, stopwords):
    """

    Args:
        file_path: absolute path of file containing text
        stopwords: Armenian stopwords path

    Json files have 2 keys
    'src' - text
    'tgt' - title of the text
     This function lemmatizes text and adds 'lemma' key
    """
    with open(file_path, 'r') as c:
        content_of_file = json.load(c)
    if 'lemma' in content_of_file.keys():
        return
    text = content_of_file['src']
    content_of_file['lemma'] = get_lemmas(text, stopwords)
    with open(file_path, 'w') as json_file:
        json.dump(content_of_file, json_file, ensure_ascii=False)


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[stopwords] [filenames]")
        return
    stopwords = u.get_filenames(sys.argv[1])
    stripped_stopwords = [s.strip() for s in stopwords]
    train_filenames = u.get_filenames(sys.argv[2])
    for file in train_filenames:
        file_path = config['folder_names'][file[0]] + file.strip()
        if os.path.exists(file_path):
            add_lemma_key(file_path, stripped_stopwords)


if __name__ == "__main__":
    main()
