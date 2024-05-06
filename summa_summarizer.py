from summa import summarizer
import sys
import os
import json
import csv


csv_filename = ''
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
    global sample, Count
    proc_text = ''
    sample['id'].append(filename)
    for sent in text:
        proc_text += " ".join(sent)
    for i in range(1, 4):
        sample['hypothesis_' + str(i)].append(summarizer.summarize(proc_text, sent_count=i))


def get_hypothesis(names, test_folder):
    with open(names, 'r') as f:
      filenames = f.readlines()
    for file in filenames:
       file_path = test_folder + '/' + file.strip()
       if os.path.exists(file_path):
          text = process_text(file_path)
          append_to_sample(file, text)


def main():
    global csv_filename
    if len(sys.argv) != 4:
        print("Specify correct arguments! - \n[test filenames] [csv filename] [test folder]")
        return
    names = sys.argv[1]
    csv_filename = sys.argv[2]
    test_folder = sys.argv[3]
    get_hypothesis(names, test_folder)
    write_to_csv()


main()
