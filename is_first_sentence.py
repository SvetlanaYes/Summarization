import csv
import os
import json
import sys
from configparser import ConfigParser

'''
Discription:
This code computes % of first 3 sentences in extracted summaries

Arguments:
argv[1] - folder with extracted summaries
'''

file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)


def process_text(filename):
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    src = content_of_file['src']
    processed_text = []
    for sentence in src:
        processed_sent = " ".join(sentence[:-1]) + ' ։ '
        processed_text.append(processed_sent)
    return processed_text


def compute_percent_of_first_sentences(hypothesis_folder):
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        count = 0
        total_count = 0
        for row in csvreader:
            file_path = config['folder_names'][row[0][0]] + row[0].strip()
            text = process_text(file_path)
            text = text[:3]
            if os.path.exists(file_path):
                if len(text) > 0:
                    total_count += 1
                    matches_top_sentences = 0
                    hypothesis = row[3].split(" ։ ")
                    # hypothesis = row[3].split(" ։") for summa_summarizer
                    for hypothesis_sentence in hypothesis:
                        for text_sentence in text:
                            processed_summary = text_sentence.replace("։", ":").strip()[:-1]
                            processed_hypothesis = hypothesis_sentence.replace("։", ":").strip()
                            if processed_hypothesis in processed_summary or processed_summary in processed_hypothesis:
                                matches_top_sentences += 1
                                break
                    if matches_top_sentences == len(hypothesis):
                        count += 1
        print(round(count * 100 / total_count, 4), "%")


def main():
    if len(sys.argv) != 2:
        print("Specify correct arguments! \n[hypothesis folder]")
        return
    hypothesis_folder = sys.argv[1]
    compute_percent_of_first_sentences(hypothesis_folder)


main()
