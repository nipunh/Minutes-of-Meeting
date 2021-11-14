'''
Train vectorizer and tokenizer to
extract 'asks for action' sentenses
from email corpus.

Current approach is straigtforward:
    - unweighted 1-2 bigrams as features
    - Stochastic Gradient Descent for classification

Required packages:
    - numpy
    - sklearn

'''
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC

import _pickle as pickle

''''
TODO:
    - proper sentenses tokenization and preprocessing
    - try prior (randomized) PCA transformation
    - try other classification approaches:
        nonlinear SVM
        perseptron
        desicion tries

'''
# fill me
stop_words = []

def get_corpus(filename):
    labs, sents = [],[]
    with open(filename) as h:
        for line in h:
            parts = line.strip().lower().split()
            if parts:
                labs.append(int(parts[0]))
                sents.append(" ".join(parts[1:]))
    return labs, sents

def save_model(model, filename='model.pkl'):
    with open(filename, 'wb') as h:
        pickle.dump(model, h)

if __name__ == '__main__':
    cv = CountVectorizer(ngram_range=(1,2),
            min_df=2,
            binary=True,
            lowercase=True,
            stop_words=stop_words)

    labs, sents = get_corpus('corpus.txt')
    X = cv.fit_transform(sents)
    Y = np.array(labs)

    train_size = int(X.shape[0]*0.8)
    X_train,X_test,Y_train,Y_test, _,test_sents = \
        train_test_split(X, Y, sents, train_size=train_size)

    sgd = SGDClassifier(alpha=0.001, verbose=2)
    svm = LinearSVC(loss='l2')


    for cls in [sgd, svm]:
        cls.fit(X_train, Y_train)
        Y_pred = cls.predict(X_test)
        print(classification_report(Y_test, Y_pred))
    
    # save vectorizer and classifier
    save_model((cv, sgd))
    
    # with open('log.txt', 'wb') as h:
    #     for y_true, y_pred, sent in zip(Y_test, Y_pred, test_sents):
    #         h.write("%d/%d\t%s\n" % (y_true, y_pred, sent))


