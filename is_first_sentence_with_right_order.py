import csv
import os
import json
import sys

folder_names = {
    '1': '/home/lab/Desktop/data/Tokenized/168tokenized/',
    'A': '/home/lab/Desktop/data/Tokenized/aravot_tokenized/',
    'I': '/home/lab/Desktop/data/Tokenized/Infocom_token/',
    'T': '/home/lab/Desktop/data/Tokenized/tokenized/'
}


def process_text(filename):
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    src = content_of_file['src']
    processed_text = []
    for sentence in src:
        processed_sent = " ".join(sentence[:-1]) + ' ։ '
        processed_text.append(processed_sent)
    return processed_text


def compute_rouge(hypothesis_folder):
    global sentence_numbers
    with open(hypothesis_folder, encoding='utf-8') as file:
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        count = 0
        total_count = 0
        for row in csvreader:
            file_path = folder_names[row[0][0]] + row[0].strip()
            text = process_text(file_path)
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
    compute_rouge(hypothesis_folder)


main()

