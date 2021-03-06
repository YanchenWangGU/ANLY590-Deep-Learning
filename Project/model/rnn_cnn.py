#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 23:33:35 2018

@author: FrankWang
"""

import pandas as pd 
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation,Bidirectional,Embedding
from keras.layers.embeddings import Embedding
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
## Plotly
import plotly.offline as py
import plotly.graph_objs as go
from keras.preprocessing import sequence
from nltk.tokenize import word_tokenize
# Others
import nltk
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import itertools
import random
from sklearn.manifold import TSNE
import string
import sklearn
from spellchecker import SpellChecker
spell = SpellChecker()

words = set(nltk.corpus.words.words())
words = set([i.lower() for i in words])
stops = set(stopwords.words("english"))

df = pd.read_csv('training_set_rel3.tsv',sep = '\t',encoding = "ISO-8859-1")

df = df[df['essay_set']<=6]

df1 = df[df['essay_set']==1]

np.unique(df1.domain1_score)

tokenized_sents = [word_tokenize(i) for i in df1.essay.tolist()]
for i in range(len(tokenized_sents)):
#    tokenized_sents[i] = [w for w in tokenized_sents[i] \
#                   if  w.lower() in words]
    tokenized_sents[i] = [t for t in tokenized_sents[i] if t not in string.punctuation]
    tokenized_sents[i] = [t.lower() for t in tokenized_sents[i]]
    tokenized_sents[i] = [w for w in tokenized_sents[i] if not w in stops and len(w) >= 3]
    

combined_word = [ " ".join(i) for i in tokenized_sents]

max_words = 2000
max_len = 300
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(combined_word)
sequences = tok.texts_to_sequences(combined_word)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
X = sequences_matrix.copy()

#######added#######3


######end############


Y = np.zeros((len(tokenized_sents), len(np.unique(df1.domain1_score))), dtype=np.uint8)
for i in range(len(tokenized_sents)):
    Y[i][df1.domain1_score.tolist()[i]-2]=1

#Y = np.array(df1.domain1_score)
random.seed(3)
rand_index = random.sample(range(len(Y)), len(Y))
X_shuffle = X[rand_index]
Y_shuffle = Y[rand_index]
split_index = int(len(Y)*0.8)
X_train = X_shuffle[:split_index,:]
Y_train = Y_shuffle[:split_index,]
X_test = X_shuffle[split_index:,:]
Y_test = Y_shuffle[split_index:,]


#def RNN():
#    inputs = Input(name='inputs',shape=[max_len])
#    layer = Embedding(max_words,50,input_length=max_len)(inputs)
#    layer = LSTM(64)(layer)
#    layer = Dense(256,name='FC1')(layer)
#    layer = Activation('relu')(layer)
#    layer = Dropout(0.5)(layer)
#    layer = Dense(1,name='out_layer')(layer)
#    layer = Activation('sigmoid')(layer)
#    model = Model(inputs=inputs,outputs=layer)
#    return model

model = Sequential()
model.add(Embedding(2000, 64, input_length=300))
model.add(LSTM(64))
model.add(Dense(256,activation='relu'))
model.add(Dense(11, activation='sigmoid'))
model.compile(optimizer=RMSprop(),loss = 'categorical_crossentropy',metrics=['accuracy'])

train_history = model.fit(X_train,Y_train,batch_size=32,epochs=40,
#          callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)],
          validation_data=[X_test, Y_test])

train_history.history['loss']
train_history.history['val_loss']


y_pred = model.predict(X_test)
#pred_matrix = y_pred.reshape(len(Y_test),11)
pred_score = []
for i in range(len(y_pred)):
    pred_score.append(np.argmax(y_pred[i])+2)


real_score = []
for i in range(len(Y_test)):
    real_score.append(np.argmax(Y_test[i])+2)




model = Sequential()
model.add(Embedding(2000, 64, input_length=300))
model.add(Conv1D(128, 5, activation='relu'))
model.add(MaxPooling1D(5))
model.add(Conv1D(128, 5, activation='relu'))
model.add(MaxPooling1D(35))
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dense(11, activation='sigmoid'))
model.compile(optimizer=RMSprop(),loss = 'categorical_crossentropy',metrics=['accuracy'])

train_history = model.fit(X_train,Y_train,batch_size=32,epochs=40,
#          callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)],
          validation_data=[X_test, Y_test])



model = Sequential()
model.add(Embedding(2000, 64, input_length=300))
model.add(Conv1D(128, 5, activation='relu'))
model.add(MaxPooling1D(5))
model.add(LSTM(64))
model.add(Dense(256,activation='relu'))
model.add(Dense(11, activation='sigmoid'))
model.compile(optimizer=RMSprop(),loss = 'categorical_crossentropy',metrics=['accuracy'])

train_history = model.fit(X_train,Y_train,batch_size=32,epochs=40,
          callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)],
          validation_data=[X_test, Y_test])


model = Sequential()
#model.add(Embedding(2000, 64, input_length=300))
#model.add(LSTM(64))
#model.add(Dense(256,activation='relu'))
model.add(Dense(11, activation='softmax'))
model.compile(optimizer=RMSprop(),loss = 'categorical_crossentropy',metrics=['accuracy'])

train_history = model.fit(X_train,Y_train,batch_size=32,epochs=40,
#          callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)],
          validation_data=[X_test, Y_test])

Y = np.array(df1.domain1_score)
random.seed(3)
rand_index = random.sample(range(len(Y)), len(Y))
X_shuffle = X[rand_index]
Y_shuffle = Y[rand_index]
split_index = int(len(Y)*0.8)
X_train = X_shuffle[:split_index,:]
Y_train = Y_shuffle[:split_index,]
X_test = X_shuffle[split_index:,:]
Y_test = Y_shuffle[split_index:,]

model = Sequential()
model.add(Embedding(2000, 64, input_length=300))
model.add(LSTM(64))
model.add(Dense(256))
model.add(Dense(1))
model.compile(optimizer=RMSprop(),loss = 'mean_squared_error')

train_history = model.fit(X_train,Y_train,batch_size=32,epochs=40,
          callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)],
          validation_data=[X_test, Y_test])