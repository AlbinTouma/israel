import json


def convert_labelstudio_spacy(labelled_data) -> list:
    pass




with open('../labelling/labelled_data/training_data.json') as f:
    labelled_data = json.load(f)

trained_data  = convert_labelstudio_spacy(labelled_data)
