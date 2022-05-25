import csv
import os
import json
from rouge import Rouge
import sys


hypothesis_folder = ''
folder_names = {
    '1': '/home/lab/Desktop/data/Tokenized/168tokenized/',
    'A': '/home/lab/Desktop/data/Tokenized/aravot_tokenized/',
    'I': '/home/lab/Desktop/data/Tokenized/Infocom_token/',
    'T': '/home/lab/Desktop/data/Tokenized/tokenized/'
}
count = 0
rouge_1 = 0
rouge_2 = 0
rouge_l = 0


def get_summary(filename):
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    tgt = content_of_file['tgt']
    summary = ''
    for i in range(len(tgt)):
        summary += ' '.join(tgt[i]) + ' '
    return summary


def rouge_score(hypothesis, summary):
    rouge = Rouge()
    score = rouge.get_scores(hypothesis, summary)[0]
    return score


def add_new_score(score):
    global rouge_1, rouge_2, rouge_l
    rouge_1 += score['rouge-1']['f']
    rouge_2 += score['rouge-2']['f']
    rouge_l += score['rouge-l']['f']


def print_results():
    global rouge_1, rouge_2, rouge_l, count
    print("rouge_1 - ", rouge_1 / count)
    print("rouge_2 - ", rouge_2 / count)
    print("rouge_l - ", rouge_l / count)


def read_csv_file(hypothesis_folder):
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
    return csvreader


def compute_rouge(hypothesis_folder):
        csvreader = read_csv_file(hypothesis_folder)
        next(csvreader)
        for row in csvreader:
            hypothesis = row[3]
            file_path = folder_names[row[0][0]] + row[0].strip()
            if os.path.exists(file_path):
                summary = get_summary(file_path)
                try:
                    score = rouge_score(hypothesis, summary)
                except ValueError:
                    continue
                add_new_score(score)
                count += 1
        print_results()


def main():
    if len(sys.argv) != 2:
        print("Specify correct arguments! \n[hypothesis folder]")
        return
    hypothesis_folder = sys.argv[1]
    compute_rouge(hypothesis_folder)
    

main()

