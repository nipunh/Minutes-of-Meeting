'''
Prepare Enrol corpus for training.
Performs clearning and sentences splitting.

Assuming corpus is placed at the './enrol' folder.

'''
import email
import os
from os import path
import re
import glob

from nltk import sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer

sent_tokenizer = PunktSentenceTokenizer()

filt = re.compile("[^A-Za-z0-9-'?.,:]+")

def clean_text(text):
    t = filt.sub(' ', str(text))
    sent = " ".join(t.split())
    # print(sent)
    return sent

email_dir_mask = 'enron/maildir/*/sent/*'

if __name__ == '__main__':
    for ef in glob.glob(email_dir_mask):
        with open(ef, 'rb') as h:
            msg = email.message_from_file(h)

        text = msg.get_payload()

        # just skip messages with plenty of useless MIME tags
        if text.find('Forwarded') > -1:
            continue

        text = clean_text(text)
        for sent in sent_tokenizer.tokenize(text):
            print(sent)

