
if __name__ == "__main__":
    print('importing libraries...')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from transformers import logging
logging.set_verbosity_error()
import pandas as pd 
import conllu
from simpletransformers.ner import NERModel, NERArgs


def make_dataframe_from_file(filepath):
    """constructs a pandas dataframe from a conllu file"""
    print(f'loading data from {filepath}')
    df = pd.DataFrame(columns=['sentence_id', 'words', 'labels'])
    
    current_sentence_id = 0
    with open(filepath, "r") as data_file:
        for tokenlist in conllu.parse_incr(data_file):
            dependencies = set([(x['head'], x['deprel'], x['id']) for x in tokenlist if not x['deprel'] == '_'])
            ### if this sentence has NO annotations, leave it out of the dataframe
            if len(dependencies) > 0:
                coordinates = [head for (head, deprel, id) in dependencies]
                conjunctions = [id for (head, deprel, id) in dependencies if id not in coordinates]
                for token in tokenlist:
                    label = 'B-COORDINATE' if token['id'] in coordinates else 'B-CONJUNCTION' if token['id'] in conjunctions else 'O'
                    row = pd.DataFrame([[current_sentence_id, token['form'], label]], columns=['sentence_id', 'words', 'labels'])
                    df = pd.concat([df, row], ignore_index=True)
            current_sentence_id += 1

    return df

def make_dataframe_from_files(filepaths):
    return pd.concat([make_dataframe_from_file(f) for f in filepaths], ignore_index=True)
    

custom_labels = ['B-COORDINATE', 'B-CONJUNCTION', 'O']

def create_model():
    model_args = NERArgs(
        num_train_epochs=3,
        learning_rate=5e-5,
        train_batch_size=16,
        eval_batch_size=16,
        no_cache=True,
        no_save=True,
        output_dir='./ml/outputs',
        overwrite_output_dir=True
    )

    model = NERModel(
        "distilbert", 
        "distilbert-base-uncased",  
        labels=custom_labels,
        args=model_args,
        use_cuda=False,
    )

    return model


if __name__ == "__main__":
    train = make_dataframe_from_files(["annotations/external/ds1-huiyu.txt.conllu"])
    test = make_dataframe_from_files(["annotations/internal/2_ian.conllu"])
    model = create_model()

    # print("Evaluating model before training:")
    # before, _, _ = model.eval_model(test, silent=True)
    # print(before)

    # print("Training model:")
    # model.train_model(train, eval_data=test)

    # print("Evaluating model after training:")
    # after, _, preds_list = model.eval_model(test, silent=True)
    # print(after)
    # print(preds_list)
