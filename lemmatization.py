import stanza
import json
import os
from configparser import ConfigParser
import sys

'''
Discription:
This code lemmatizes train texts, and adds lemma keys to train json files
'''

file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)
nlp = stanza.Pipeline('hy', tokenize_pretokenized=True, processors='tokenize,lemma')


def get_lemmas(text, stopwords):
    a = []
    processed_text = nlp(text)
    for s in processed_text.sentences:
        for w in s.words:
            if w.lemma not in stopwords:
               a.append(w.lemma)
    return a


def add_lemma_key(file_path, stopwords):
    with open(file_path, 'r') as c:
        content_of_file = json.load(c)
    if 'lemma' in content_of_file.keys():
        return
    text = content_of_file['src']
    content_of_file['lemma'] = get_lemmas(text, stopwords)
    with open(file_path, 'w') as json_file:
        json.dump(content_of_file, json_file, ensure_ascii=False)


def read_file(file):
    with open(file, 'r') as s:
        content = s.readlines()
    return content


def process_stopwords(stopwords):
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].strip()
    return stopwords


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[stopwords] [train filenames]")
        return
    stopwords = read_file(sys.argv[1])
    stopwords = process_stopwords(stopwords)
    train_filenames = read_file(sys.argv[2])
    for file in train_filenames:
        file_path = config['folder_names'][file[0]] + file.strip()
        if os.path.exists(file_path):
            add_lemma_key(file_path, stopwords)


if __name__ == "__main__":
    main()
