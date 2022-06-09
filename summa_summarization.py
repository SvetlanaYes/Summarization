# TODO: refactor and improve code
from summa.summarizer import summarize
import sys
import os
import json
import csv


csv_filename = ''
folder_names = {
    '1': '/home/lab/Desktop/data/Tokenized/168tokenized/',
    'A': '/home/lab/Desktop/data/Tokenized/aravot_tokenized/',
    'I': '/home/lab/Desktop/data/Tokenized/Infocom_token/',
    'T': '/home/lab/Desktop/data/Tokenized/tokenized/'
}
keys = ['id', 'hypothesis_1', 'hypothesis_2', 'hypothesis_3']
sample = {
          "id": [],
          "hypothesis_1": [],
          "hypothesis_2": [],
          "hypothesis_3": []
          }


def write_to_csv():
    global sample, csv_filename
    with open(csv_filename, "w", encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        writer.writerow(keys)
        writer.writerows(zip(*[sample[key] for key in keys]))


def process_text(filename):
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    src = content_of_file['src']
    return src


def append_to_sample(filename, text):
    global sample
    sample['id'].append(filename)
    sample['hypothesis_1'].append(summarize(text, sent_count=1))
    sample['hypothesis_2'].append(summarize(text, sent_count=2))
    sample['hypothesis_3'].append(summarize(text, sent_count=3))


def get_hypothesis(names):
    with open(names, 'r') as f:
      filenames = f.readlines()
    for file in filenames:
       file_path = folder_names[file[0]] + file.strip()
       if os.path.exists(file_path):
          text = process_text(file_path)
          append_to_sample(file, text)
    write_to_csv()


def main():
    if len(sys.argv) != 3:
        print("Specify correct arguments! - [test filenames] [.csv filename]")
        return
    names = sys.argv[1]
    csv_filename = sys.argv[2]
    get_hypothesis(names)


main()

