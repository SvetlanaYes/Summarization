# TODO: refactor and improve code
import csv
import os
import json
from rouge import Rouge
import sys


"""
Discription:

This code computes rouge of extracted summary and title for every text example.
Prints average of rouge_1, rouge_2, rouge_l

Arguments:

argv[1] - file with extracted hypothesises
argv[2] - count of sentences extracted from text (1,2,3)

hypothesis file format is csv

    1st row contains ID of file with original text
    2nd row contains extracted summary with 1 sentence
    3rd row contains extracted summary with 2 sentences
    4th row contains extracted summary with 3 sentences
"""

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


def get_title(filename):
    """
    Discription:
    Function extracts title from file.
    File format is json
    ['tgt'] - title

    Arguments:
    filename 
    
    Returning value: string
    Returns: title 
    """
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    tgt = content_of_file['tgt']
    title = ''
    for sentence in tgt:
        title += ' '.join(sentence) + ' '
    return title


def rouge_score(hypothesis, title):
    rouge = Rouge()
    score = rouge.get_scores(hypothesis, title)[0]
    return score


def add_new_score(score):
    global rouge_1, rouge_2, rouge_l
    rouge_1 += score['rouge-1']['f']
    rouge_2 += score['rouge-2']['f']
    rouge_l += score['rouge-l']['f']


def print_results():
    """
    Discription:
    Function prints average of rouge_1 rouge_2 rouge_l
    """
    global rouge_1, rouge_2, rouge_l, count
    print("rouge_1 - ", rouge_1 / count)
    print("rouge_2 - ", rouge_2 / count)
    print("rouge_l - ", rouge_l / count)


def read_csv_file(hypothesis_folder):
    """
    Discription:
    Function reads from csv file
    
    Arguments:
    hypothesis_folder - csv file

    Returning value: list
    Returns:
    [0] - name of file
    [1] - hypothesis with 1 sentence
    [2] - hypothesis with 2 sentences
    [3] - hypothesis with 3 sentences
    """
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
    return csvreader


def compute_rouge(hypothesis_folder, count_of_extracted_sentences):
    """ 
    Discription:
    Function computes rouge of extracted summary and title

    Arguments:
    hypothesis_folder - csv file
    count_of_extracted_sentences - count of extracted sentences from text (1,2,3)
    """
    csvreader = read_csv_file(hypothesis_folder)
    next(csvreader)
    for row in csvreader:
        hypothesis = row[count_of_extracted_sentences]
        absolute_file_path = folder_names[row[0][0]] + row[0].strip()
        if os.path.exists(absolute_file_path):
            title = get_title(absolute_file_path)
            try:
                score = rouge_score(hypothesis, title)
            except ValueError:
                """this error occures when original text is empty"""
                continue
            add_new_score(score)
            count += 1
    print_results()


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[hypothesis folder], [count of extracted sentences]\n")
        return
    hypothesis_folder = sys.argv[1]
    count_of_extracted_sentences = sys.argv[2]
    compute_rouge(hypothesis_folder, count_of_extracted_sentences)
    

main()
