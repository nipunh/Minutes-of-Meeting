import spacy
from pprint import pprint
import nltk

nlp = spacy.load('en_core_web_sm')
sent = "All of you are to do that"
doc=nlp(sent)

sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]

print(sub_toks) 
pprint([(X.text, X.label_) for X in doc.ents])

tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

text = '''If we are all here, let's get started. First of all, I'd like you to please join me in welcoming Jack Peterson, our Southwest Area Sales Vice President.'''
olo = tokenizer.tokenize(text)
pprint(olo)