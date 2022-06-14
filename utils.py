import json
from rouge import Rouge
from configparser import ConfigParser


file = 'config.ini'
config = ConfigParser()
config.optionxform = lambda option: option
config.read(file)


def get_filenames(names):
    """
    Discription:
    Function gets  filenames from given file

    Arguments:
    names - file with filenames

    Returning value: list
    Retruns: filenames
    """
    with open(names, 'r') as f:
        filenames = f.readlines()
    return filenames


def process_text_to_list(filename):
    with open(filename, 'r') as d:
        content_of_file = json.load(d)
    src = content_of_file['src']
    processed_text = []
    for sentence in src:
        processed_sent = " ".join(sentence[:-1]) + ' ։ '
        processed_text.append(processed_sent)
    return processed_text


def rouge_score(hypothesis, summary):
    rouge = Rouge()
    score = rouge.get_scores(hypothesis, summary)[0]
    return score


def get_absolute_path(row):
    return config['folder_names'][row[0][0]] + row[0].strip()
