from transformers import logging, AutoConfig, AutoTokenizer, AutoModel
from summarizer import Summarizer
import json
import os
import csv
import sys

model = ''
keys = ['id', 'hypothesis_1', 'hypothesis_2', 'hypothesis_3']
sample = {
          "id": [],
          "hypothesis_1": [],
          "hypothesis_2": [],
          "hypothesis_3": []
          }
csv_filename = ''


def set_model(bert_model):
    global model
    logging.set_verbosity_error()
    custom_config = AutoConfig.from_pretrained(bert_model)
    custom_config.output_hidden_states = True
    custom_tokenizer = AutoTokenizer.from_pretrained(bert_model)
    custom_model = AutoModel.from_pretrained(bert_model, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)


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
    processed_text = ""
    for sentence in src:
        if sentence[-1] == ":" or sentence[-1] == "։":
            processed_text += ' '.join(sentence[:-1]) + ' ։ '
        else:
            processed_text += ' '.join(sentence) + ' ։ '
    return processed_text


def append_to_sample(filename, text):
    global sample
    sample['id'].append(filename)
    sample['hypothesis_1'].append(model(text, num_sentences=1))
    sample['hypothesis_2'].append(model(text, num_sentences=2))
    sample['hypothesis_3'].append(model(text, num_sentences=3))


def get_filenames(names):
    with open(names, 'r') as f:
      filenames = f.readlines()
    return filenames


def get_hypothesis(names):
    count = 0
    filenames = get_filenames(names)
    for file in filenames:
       absolute_file_path = '/home/lab/Desktop/test_10000/' + file.strip()
       if os.path.exists(absolute_file_path):
          text = process_text(absolute_file_path)
          append_to_sample(file, text)
    write_to_csv()


def main():
    if len(sys.argv) != 4:
        print("Specify correct arguments! \n[test filenames] [model name] [csv filename]")
        return
    names = sys.argv[1]
    bert_model_name = sys.argv[2]
    csv_filename = sys.argv[3]
    set_model(bert_model_name)
    get_hypothesis(names)


main()

