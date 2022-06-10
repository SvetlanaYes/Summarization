import csv
import os
import json
import sys
from configparser import ConfigParser
import utils as u
'''
Discription:
This code computes % of first 3 sentences in extracted summaries in the right order

Arguments:
argv[1] - folder with extracted summaries
'''

file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)


def compute_percent_of_first_sentences(hypothesis_folder):
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        count = 0
        total_count = 0
        for row in csvreader:
            file_path = config['folder_names'][row[0][0]] + row[0].strip()
            text = u.process_text_to_list(file_path)
            if os.path.exists(file_path):
                if len(text) > 0:
                    total_count += 1
                    matches_top_sentences = True
                    hypothesis = row[3].split(" ։ ")
                    # hypothesis = row[3].split(" ։") for summa_summrizer
                    if len(text) < len(hypothesis):
                        continue
                    else:
                        for i, sentence in enumerate(hypothesis):
                            processed_summary = text[i].replace("։", ":").strip()[:-1]
                            processed_hypothesis = sentence.replace("։", ":").strip()
                            if (processed_hypothesis not in processed_summary
                                    and processed_summary not in processed_hypothesis):
                                matches_top_sentences = False
                                break
                        count += int(matches_top_sentences)
        print(round(count * 100 / total_count, 4), "%")


def main():
    if len(sys.argv) != 2:
        print("Specify correct arguments! \n[hypothesis folder]")
        return
    hypothesis_folder = sys.argv[1]
    compute_percent_of_first_sentences(hypothesis_folder)


if __name__ == "__main__":
    main()
