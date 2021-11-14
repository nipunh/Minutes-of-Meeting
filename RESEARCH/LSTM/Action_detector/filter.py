import sys
from corpus import clean_text, sent_tokenizer
import _pickle as pickle
import spacy
from pprint import pprint
nlp = spacy.load('en_core_web_sm')

def process(filename, model):
    vect, cls = model

    final_sents = []
    final_sents_with_tags = []
    subjects = []
    action_items = []
    tags = []
    sentences = []
    with open(filename) as h:
        data = h.read()
        data = data.splitlines()        
        for i in range(len(data)):
            sep = data[i].split(':')
            tags.append(sep[0])
            print(sep[0])
            sentences.append(sep[1])
        text = clean_text(sentences)
        sents = sent_tokenizer.tokenize(text)

    for i in range(len(sents)):
        # final_sents_with_tags.append(sent)
        final_sents.append(sents[i])

    X = vect.transform(final_sents)
    Y = cls.predict(X)


    for sent, y in zip(final_sents, Y):
        print('+' if y else ' ','\t', sent)
        if(y):
            doc = nlp(sent)
            sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
            print(sub_toks) 
            you = [i for i in sub_toks if str(i) == 'you']
            if(len(you) >= 1):
                final_sents_with_tags.append([you, sent])
            action_items.append([[(X.text, X.label_) for X in doc.ents], str(sent)])

    # print(action_items[0][0][0][1])
    # print(action_items)
    
    print(final_sents_with_tags)
    print(len(final_sents_with_tags))

    for item in action_items:
        try:
            if(item[0][0][1] != 'PLACE_HOLDER'):
                subjects.append(item[0][0][0])

        except:
            pass

    print(subjects)
    cleaned_text = []
    k = 0
    for i in range(len(tags)):
        clean_sent = clean_text(sentences[i])
        try:
            print(str(action_items[k][1])[5:], len(str(action_items[k][1])[5:]), str(clean_sent), len(str(clean_sent)))
            if(str(action_items[k][1])[5:] == str(clean_sent)):
                k += 1
                cleaned_text.append([str(clean_sent), tags[i+2]])
                print(k)
        except:
            pass

    print(cleaned_text)
    print(len(cleaned_text))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage %s: <filename>" % sys.argv[0])

    filename = sys.argv[1]

    with open('model.pkl', 'rb') as h:
        model = pickle.load(h)

    process(filename, model)
