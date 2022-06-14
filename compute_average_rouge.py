import csv
import os
import json
from rouge import Rouge
import sys
from configparser import ConfigParser
import utils as u


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

file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)


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


def add_new_score(score, rouge_1, rouge_2, rouge_l):
    rouge_1 += score['rouge-1']['f']
    rouge_2 += score['rouge-2']['f']
    rouge_l += score['rouge-l']['f']
    return rouge_1, rouge_2, rouge_l


def print_results(rouge_1, rouge_2, rouge_l, count):
    """
    Discription:
    Function prints average of rouge_1 rouge_2 rouge_l
    """
    print("rouge_1 - ", rouge_1 / count)
    print("rouge_2 - ", rouge_2 / count)
    print("rouge_l - ", rouge_l / count)


def compute_rouge(hypothesis_folder, count_of_extracted_sentences):
    """ 
    Discription:
    Function computes rouge of extracted summary and title

    Arguments:
    hypothesis_folder - csv file
    count_of_extracted_sentences - count of extracted sentences from text (1,2,3)
    """
    count = 0
    rouge_1 = 0
    rouge_2 = 0
    rouge_l = 0
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        for row in csvreader:
            hypothesis = row[count_of_extracted_sentences]
            absolute_file_path = config['folder_names'][row[0][0]] + row[0].strip()
            if os.path.exists(absolute_file_path):
                title = get_title(absolute_file_path)
                if not hypothesis or not title:
                    continue
                score = u.rouge_score(hypothesis, title)
                rouge_1, rouge_2, rouge_l = add_new_score(score, rouge_1, rouge_2, rouge_l)
                count += 1
    print_results(rouge_1, rouge_2, rouge_l, count)


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! \n[hypothesis folder], [count of extracted sentences]\n")
        return
    hypothesis_folder = sys.argv[1]
    count_of_extracted_sentences = int(sys.argv[2])
    compute_rouge(hypothesis_folder, count_of_extracted_sentences)


if __name__ == "__main__":
    main()
