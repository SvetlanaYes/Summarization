import csv
import os
import sys
import utils as u
'''
Discription:
This code computes % of first 3 sentences in extracted summaries

Arguments:
argv[1] - folder with extracted summaries
'''


def compute_percent_of_first_sentences(hypothesis_folder):
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        count = 0
        total_count = 0
        for row in csvreader:
            file_path = u.get_absolute_path(row)
            text = u.process_text_to_list(file_path)
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


if __name__ == "__main__":
    main()
