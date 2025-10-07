# SpaCy requires training data in a specific format. 
# The convert_labelstudio_spacy function converts labelstudio fields from training data json into the right format.

import json
import spacy
from spacy.tokens import DocBin, Doc

if not Doc.has_extension("rel"):
    Doc.set_extension("rel", default={})

def convert_labelstudio_spacy(labelled_data, nlp) -> list:
    """Converts training data into the right format from labelstudio json file to spaCy format"""

    db = DocBin()
    for task in labelled_data:
        text = task['data']['content']
        annotations = task['annotations'][0]['result']
        doc = nlp.make_doc(text)

        entities = []
        entity_map = {}
        
        #get entities
        for ann in annotations:
            if ann['type'] == 'labels':
                start = ann['value']['start']
                end = ann['value']['end']
                label = ann['value']['labels'][0]
                ent_id = ann["id"]
                span = doc.char_span(start, end, label=label, alignment_mode='contract')
                if span is None:
                    print(f"Skipping entity: {text[start:end]}")
                else:
                    entities.append(span)
                    entity_map[ent_id] = len(ents) - 1

            doc.ents = ents

            rels = {}
            for ann in annotations:
                if ann['type'] == 'relation':
                    from_id = ann['from_id']
                    to_id = ann["to_id"]
                    rel_label = ann['labels'][0]

                    if from_id in entity_map and to_id in entity_map:
                        head = ents[entity_map[from_id]]
                        tail = ents[entity_map[to_id]]
                        rels[(head.start, tail.start)] = {"label": rel_label}


            doc._.rel = rels

            db.add(doc)
        return db





with open('../labelling/labelled_data/training_data.json') as f:
    labelled_data = json.load(f)

nlp = spacy.blank('en')
db  = convert_labelstudio_spacy(labelled_data, nlp)
db.to_disk('./train.spacy')
