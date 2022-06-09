import json
import pickle
import os
import numpy as np
from rouge import Rouge
import sys

"""
Discription:
Code computes scores of sentences for every text, and extracts top sentences as summary.

Arguments:
argv[1] - tfidf pickeled model path
argv[2] - file with test filenames
argv[3] - absolute path of directory which contains lemmatized texts
argv[4] - count of sentences to extract as summary
"""



def process_title(text):
    processed_text = ''
    for i in range(len(text)):
        processed_text += ' '.join(text[i]) + ' '
    return processed_text


def process_sentence(text):
    processed_text = ''
    for i in range(len(text)):
        processed_text += ''.join(text[i]) + ' '
    return processed_text


def rouge_score(hypothesis, summary):
    rouge = Rouge()
    score = rouge.get_scores(hypothesis, summary)[0]
    return score


def print_results(sample):
    for key in sample:
        print(key)
        print("rouge_1 - ", sample[key][0] / sample[key][3])
        print("rouge_2 - ", sample[key][1] / sample[key][3])
        print("rouge_l - ", sample[key][2] / sample[key][3])


def load_model(model):
    with open(model, 'rb') as f:
        tf_idf_model = pickle.load(f)
    return tf_idf_model


def get_test_filenames(file):
    with open(file, 'r') as f:
        file_names = f.readlines()
    return file_names


def get_hypothesis(text, scores):
    hypothesis = []
    sentence = ''
    for i in range(0, 3):
        if len(text) >= i + 1:
            sentence += process_sentence(text[np.argmax(scores)])
            hypothesis.append(sentence)
            scores[np.argmax(scores)] = -1
        else:
            break
    return hypothesis


def process_lemma(text):
    processed_text = ''
    for word in text:
        processed_text += ''.join(word) + ' '
    return processed_text


def compute_rouge(hypothesis, title, sample):
    for i, sentence in enumerate(hypothesis):
        score = rouge_score(sentence, title)
        sample[i + 1][0] += score["rouge-1"]["f"]
        sample[i + 1][1] += score["rouge-2"]["f"]
        sample[i + 1][2] += score["rouge-l"]["f"]
        sample[i + 1][3] += 1
    return sample


def extract_summary(tf_idf_model, test_filenames, test_files_directory):
    sample = {
        1: [0, 0, 0, 0],
        2: [0, 0, 0, 0],
        3: [0, 0, 0, 0]
    }
    for i, file in enumerate(test_filenames):
        full_path = test_files_directory + file.strip()
        with open(full_path, 'r') as f:
            content_of_file = json.load(f)
        scores = []
        if len(content_of_file['src']) == 0:
            continue
        lemma = process_lemma(content_of_file['lemma'])
        if ' : ' in lemma:
            lemma = lemma.split(" : ")[:-1]
        else:
            lemma = lemma.split(" ։ ")
        if len(lemma) == 0:
            continue
        if len(lemma[-1]) == 0:
            lemma.pop()
        for sentence in lemma:
            proc_sentence = process_sentence(sentence)
            with open('tmp.txt', 'w') as t:
                t.write(proc_sentence)
            tmp_file = [os.getcwd() + '/tmp.txt']
            word_scores = tf_idf_model.transform(tmp_file)
            total = np.sum(word_scores.toarray())
            scores.append(total)
        hypothesis = get_hypothesis(content_of_file['src'], scores)
        if len(hypothesis) == 0:
            continue
        title = process_title(content_of_file['tgt'])
        sample = compute_rouge(hypothesis, title, sample)
    return sample


def main():
    if len(sys.argv) != 4:
        print("Specify correct arguments! \n [tfidf model] [test filenames] [absolute path of test files directory]\n")
        return
    tf_idf_model = load_model(sys.argv[1])
    test_filenames = get_test_filenames(sys.argv[2])
    test_files_directory = sys.argv[3]
    tf_idf_rouge_scores = extract_summary(tf_idf_model, test_filenames, test_files_directory)
    print_results(tf_idf_rouge_scores)


main()
