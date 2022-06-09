from transformers import logging, AutoConfig, AutoTokenizer, AutoModel
from summarizer import Summarizer
import json
import os
import csv
import sys

"""
Discription:

This code gets texts from given files and extracts summaries(1,2,3 sentences) using given model.

Arguments:

argv[1] -> file of filenames
argv[2] -> model name
argv[3] -> csv filename to save results

"""


def set_model(model_name):
    """
    Discription:
    Function sets Summarizer custom_model = given model and custom_tokenizer = Autotokenizer.from_pretrained(given model)
    
    Arguments:
    bert_model - given name model
    """
    logging.set_verbosity_error()
    custom_config = AutoConfig.from_pretrained(model_name)
    custom_config.output_hidden_states = True
    custom_tokenizer = AutoTokenizer.from_pretrained(model_name)
    custom_model = AutoModel.from_pretrained(model_name, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    return model


def write_to_csv(csv_filename, sample):
    """
    Discription:
    Function to save list of exracted sentences in csv file
    1st row - name of file
    2nd row - list of extracted summaries with 1 sentence
    3rd row - list of extracted summaries with 2 sentences
    4th row - list of extracted summaries with 3 sentences
    """
    keys = ['id', 'hypothesis_1', 'hypothesis_2', 'hypothesis_3']
    with open(csv_filename, "w", encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        writer.writerow(keys)
        writer.writerows(zip(*[sample[key] for key in keys]))


def process_text(filename):
    """
    Discription:
    Function processed texts in given files.

    Arguments:
    filename - absolute path of file with text and title.

    File format is json:
    ['src'] - text
    ['tgt'] - text title 

    Returning value: string
    Returns: processed text
    """
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


def get_filenames(names):
    """
    Discription:
    Function gets test filenames from given file

    Arguments:
    names - file with test filenames

    Returning value: list
    Retruns: test filenames
    """
    with open(names, 'r') as f:
        filenames = f.readlines()
    return filenames


def get_hypothesis(names, test_folder, model):
    """
    Discription:
    Function extracts summaries from texts 

    Arguments:
    names - file with test filenames
    """
    sample = {
        "id": [],
        "hypothesis_1": [],
        "hypothesis_2": [],
        "hypothesis_3": []
    }
    filenames = get_filenames(names)
    for file in filenames:
        absolute_filepath = test_folder + '/' + file.strip()
        if os.path.exists(absolute_filepath):
            text = process_text(absolute_filepath)
            sample['id'].append(file)
            sample['hypothesis_1'].append(model(text, num_sentences=1))
            sample['hypothesis_2'].append(model(text, num_sentences=2))
            sample['hypothesis_3'].append(model(text, num_sentences=3))
    return sample


def main():
    if len(sys.argv) != 5:
        print("Specify correct arguments! \n[test filenames] [model name] [csv filename] [test folder]")
        return
    names = sys.argv[1]
    model = set_model(sys.argv[2])
    csv_filename = sys.argv[3]
    test_folder = sys.argv[4]
    id_hypothesises = get_hypothesis(names, test_folder, model)
    write_to_csv(csv_filename, id_hypothesises)


main()
