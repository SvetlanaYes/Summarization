import json
import pickle
import os
import numpy as np
from rouge import Rouge


pwd = os.getcwd()
test_file_names = '/home/lab/Desktop/bert_distilBert/files/test_rand_10000.txt'
directory = '/home/lab/Desktop/test_10000/'
count = 0
rouge_1 = 0
rouge_2 = 0
rouge_l = 0


def process_sentence(text):
    processed_text = ''
    for i in range(len(text)):
        processed_text += ''.join(text[i]) + ' '
    return processed_text


def process_target(text):
    processed_text = ''
    for i in range(len(text)):
        processed_text += ' '.join(text[i]) + ' '
    return processed_text


def rouge_score(hypothesis, summary):
    rouge = Rouge()
    score = rouge.get_scores(hypothesis, summary)[0]
    return score


def print_results():
    global rouge_1, rouge_2, rouge_l, count
    print("rouge_1 - ", rouge_1 / count)
    print("rouge_2 - ", rouge_2 / count)
    print("rouge_l - ", rouge_l / count)


def add_scores(score):
    global rouge_1, rouge_2, rouge_l
    rouge_1 = rouge_1 + score["rouge-1"]["f"]
    rouge_2 = rouge_2 + score["rouge-2"]["f"]
    rouge_l = rouge_l + score["rouge-l"]["f"]


with open('/home/lab/Desktop/bert_distilBert/files/model_pkl', 'rb') as f:
    tf_idf_model = pickle.load(f)

with open(test_file_names, 'r') as f:
    file_names = f.readlines()

for file in file_names:
    full_path = directory + file.strip()
    with open(full_path, 'r') as f:
        content_of_file = json.load(f)
    scores = []
    for i in range(len(content_of_file['src'])):
        proc_sentence = process_sentence(content_of_file['src'][i])
        with open('tmp.txt', 'w') as t:
            t.write(proc_sentence)
        file = [pwd + '/tmp.txt']
        word_scores = tf_idf_model.transform(file)
        total = np.sum(word_scores.toarray())
        scores.append(total)
    if len(content_of_file['src']) == 0:
        continue
    hypothesis = process_sentence(content_of_file['src'][np.argmax(scores)])
    # scores[np.argmax(scores)] = -1
    # hypothesis += process_sentence(content_of_file['src'][np.argmax(scores)])
    # scores[np.argmax(scores)] = -1
    # hypothesis += process_sentence(content_of_file['src'][np.argmax(scores)])
    summary = process_target(content_of_file['tgt'])
    try:
        score = rouge_score(hypothesis, summary)
    except ValueError:
        with open('/home/lab/Desktop/bert_distilBert/summary_errors.txt', 'a') as s:
            s.write(file)
            continue
    add_scores(score)
    count += 1
print_results()

