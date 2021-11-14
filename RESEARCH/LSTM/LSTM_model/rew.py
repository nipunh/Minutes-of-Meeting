from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import os
import pickle
import pandas as pd
from nltk import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
import re

sent_tokenizer = PunktSentenceTokenizer()

def clean_text(text):
    filt = re.compile("[^A-Za-z0-9-'?.,:]+")
    t = filt.sub(' ', text)
    return " ".join(t.split())

with open('test.txt') as h:
    text = clean_text(h.read())
    sents = sent_tokenizer.tokenize(text)


with open('apollo25.json', 'r') as json_file:
    loaded_model_json = json_file.read()

loaded_model = model_from_json(loaded_model_json)

# train_path = 'train.csv'
# train_df = pd.read_csv(train_path)

# X_train = train_df["sentence"].fillna("fillna").values

loaded_model.load_weights("model225.h5")

# Tokenizer = Tokenizer()
# texts = X_train
# Tokenizer.fit_on_texts(texts)

# tokenizer = Tokenizer
with open('tokenizer25.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

for k in range(len(sents)):
    phrase = sents[k]
    
    tokens = tokenizer.texts_to_sequences([phrase])
    tokens = pad_sequences(tokens, maxlen=4000)
    prediction = loaded_model.predict(np.array(tokens))
    i,j = np.where(prediction == prediction.max()) 
    i = int(i)
    j = int(j)
    # print(prediction)
    
    total_possible_outcomes = ["1yes","2no"]
    print("String: ", sents[k], "\tResult:",total_possible_outcomes[j])
