import csv
import os
import sys
import utils as u
'''
Discription:
This code computes % of first 3 sentences in extracted summaries in the right order

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
            if os.path.exists(file_path):
                if len(text) > 0:
                    total_count += 1
                    matches_top_sentences = True
                    hypothesis = row[3].replace(":", "։").split(" ։ ")
                    # hypothesis = row[3].replace(":", "։").split("\n") for tf-idf
                    # hypothesis = row[3].replace(":", "։").split(" ։") for summa_summrizer
                    if len(text) < len(hypothesis):
                        continue
                    else:
                        for i, sentence in enumerate(hypothesis):
                            processed_summary = text[i].replace(":", "։").strip()
                            processed_hypothesis = sentence.strip()
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
