# TODO: refactor and improve code
import stanza
import json
import os

stopwords_folder = '/home/lab/Desktop/bert_distilBert/stop_words_hy.txt'
train_data_names = '/home/lab/Desktop/bert_distilBert/data/train.txt'
folder_names = {
    '1': '/home/lab/Desktop/data/Tokenized/168tokenized/',
    'A': '/home/lab/Desktop/data/Tokenized/aravot_tokenized/',
    'I': '/home/lab/Desktop/data/Tokenized/Infocom_token/',
    'T': '/home/lab/Desktop/data/Tokenized/tokenized/'
}

with open(stopwords_folder, 'r') as s:
    stopwords = s.readlines()

with open(train_data_names, 'r') as d:
    train_data = d.readlines()

nlp = stanza.Pipeline('hy', tokenize_pretokenized=True, processors='tokenize,lemma')


def get_lemmas(text):
    a = []
    processed_text = nlp(text)
    for s in processed_text.sentences:
        for w in s.words:
            a.append(w.lemma)
    return a


def add_lemma_key(file_path):
    with open(file_path, 'r') as c:
        content_of_file = json.load(c)
    if 'lemma' in content_of_file.keys():
        return
    text = content_of_file['src']
    content_of_file['lemma'] = get_lemmas(text)
    with open(file_path, 'w') as json_file:
        json.dump(content_of_file, json_file, ensure_ascii=False)


for file in train_data:
    file_path = folder_names[file[0]] + file.strip()
    if os.path.exists(file_path):
        add_lemma_key(file_path)

