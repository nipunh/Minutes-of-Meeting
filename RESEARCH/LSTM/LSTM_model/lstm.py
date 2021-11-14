import pandas as pd
import numpy as np
import os
from random import shuffle
import pickle
from keras.optimizers import SGD, Adam, Nadam, RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.preprocessing import sequence
from keras.models import Sequential,Model,load_model
from keras.layers import Embedding,Conv1D,MaxPooling1D
from keras.layers.core import Dense, Activation,Dropout ,Flatten
from keras.layers.recurrent import LSTM
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence,one_hot,Tokenizer
from keras.constraints import maxnorm
from keras.callbacks import ModelCheckpoint,TensorBoard, ReduceLROnPlateau,EarlyStopping
from keras.applications import Xception
from keras import regularizers
from keras import backend as K
import keras
import numpy as np
import pandas as pd
import cv2
import os
import glob
import math
import matplotlib.pyplot as plt

# seed = 120
# np.random.seed(seed)

train_path = 'training.csv'
train_df = pd.read_csv(train_path)

test_path = 'testing.csv'
test_df = pd.read_csv(test_path)

X_train = train_df["sentence"].fillna("fillna").values
y_train = train_df[["yes","no"]].values

X_test = test_df["sentence"].fillna("fillna").values
y_test = test_df[["yes","no"]].values

Tokenizer = Tokenizer()

texts = X_train

Tokenizer.fit_on_texts(texts)
Tokenizer_vocab_size = len(Tokenizer.word_index) + 1

print(X_train.shape, y_train.shape)

maxWordCount= 4000
maxDictionary_size=Tokenizer_vocab_size

X_train = X_train
y_train = y_train

X_val = X_test
y_val = y_test

X_train_encoded_words = Tokenizer.texts_to_sequences(X_train)
X_val_encoded_words = Tokenizer.texts_to_sequences(X_val)

X_train_encoded_padded_words = sequence.pad_sequences(X_train_encoded_words, maxlen=maxWordCount)
X_val_encoded_padded_words = sequence.pad_sequences(X_val_encoded_words, maxlen=maxWordCount)


#model
model = Sequential()

model.add(Embedding(maxDictionary_size, 32, input_length=maxWordCount)) #to change words to ints
# model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
# model.add(MaxPooling1D(pool_size=2))
# model.add(Dropout(0.5))
# model.add(Conv1D(filters=32, kernel_size=2, padding='same', activation='relu'))
# model.add(MaxPooling1D(pool_size=2))
 #hidden layers
model.add(LSTM(20))
# model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(1200, activation='relu',W_constraint=maxnorm(1)))
# model.add(Dropout(0.6))
model.add(Dense(500, activation='relu',W_constraint=maxnorm(1)))
model.add(Dense(400, activation='relu',W_constraint=maxnorm(1)))
# model.add(Dropout(0.5))
 #output layer
model.add(Dense(2, activation='softmax'))

# Compile model
# adam=Adam(lr=learning_rate, beta_1=0.7, beta_2=0.999, epsilon=1e-08, decay=0.0000001)

print(model.summary())


learning_rate=0.005
epochs = 15
batch_size = 48 #32
sgd = SGD(lr=learning_rate, nesterov=True, momentum=0.7, decay=1e-4)
Nadam = keras.optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004)
model.compile(loss='categorical_crossentropy', optimizer=Nadam, metrics=['accuracy'])

# print(X_train_encoded_padded_words.shape)
# print(y_train.shape)

# print(X_val_encoded_padded_words.shape)
# print(y_val.shape)

history  = model.fit(X_train_encoded_padded_words,y_train, epochs = epochs, batch_size=batch_size, 
            verbose=1, validation_data=(X_val_encoded_padded_words, y_val))

score = model.evaluate(X_val_encoded_padded_words, y_val, verbose=1)
print('Test accuracy:', score[1],'%')

phrase = "Do that work by tomorrow"
tokens = Tokenizer.texts_to_sequences([phrase])
tokens = pad_sequences(tokens, maxlen=4000)
prediction = model.predict(np.array(tokens))
i,j = np.where(prediction == prediction.max()) #calculates the index of the maximum element of the array across all axis
# i->rows, j->columns
i = int(i)
j = int(j)
print(prediction)
total_possible_outcomes = ["1yes","2no"]
print("Result:",total_possible_outcomes[j])


# serialize model to JSON
model_json = model.to_json()
with open("apollo25.json", "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights("model225.h5")
print("Saved model to disk")

# saving
with open('tokenizer25.pickle', 'wb') as handle:
    pickle.dump(Tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)