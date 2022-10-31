# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 15:59:18 2022

@author: cflorelu
"""

#¿Qué es el reconocimiento de entidades con nombre?

#Tarea de NLP para identificar entidades con nombre importantes en el texto:
    
    #personas, lugares, organizaciones, fechas, estados, obras de arte... 
    
    #¡y otras categorías! Puede utilizarse junto con la identificación del tema... o por sí sola.
    
#La biblioteca Stanford Core NLP

#Integrada en Python mediante nltk

#Soporte para NER, así como árboles de coreferencia y dependencia
import pandas as pd

import nltk
nltk.download("punkt")
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk.tokenize import word_tokenize

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import TweetTokenizer #The nltk.tokenize.TweetTokenizer class gives you some extra methods and attributes for parsing tweets.

import matplotlib.pyplot as plt
from collections import defaultdict

with open('data_examples/articles.txt', encoding='utf8') as f:
    corpus = f.read()
    print(corpus)

# Tokenize the article into sentences: sentences
sentences = nltk.sent_tokenize(corpus)

# Tokenize each sentence into words: token_sentences
token_sentences = [nltk.word_tokenize(sent) for sent in sentences]

# Tag each tokenized sentence into parts of speech: pos_sentences
pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences] 

# Create the named entity chunks: chunked_sentences
chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True)

# Test for stems of the tree with 'NE' tags
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, "label") and chunk.label() == "NE":
            print(chunk)     

# Create the defaultdict: ner_categories
ner_categories = defaultdict(int)

# Create the nested for loop
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label'):
            ner_categories[chunk.label()] += 1
            
# Create a list from the dictionary keys for the chart labels: labels
labels = list(ner_categories.keys())

# Create a list of the values: values
values = [ner_categories.get(v) for v in labels]

# Create the pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

# Display the chart
plt.show()

# -- Intro a SpaCy -- #

# Import spacy
import spacy

# Instantiate the English model: nlp
nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'matcher'])

# Create a new document: doc
doc = nlp(corpus)
     
# Print all of the found entities and their labels
for ent in doc.ents:
    print(ent.label_, ent.text)

# --Polyglot -- #
from polyglot.text import Text

# Create a new text object using Polyglot's Text class: txt
txt = Text(corpus)

# Print each of the entities found
for ent in txt.entities:
    print(ent)
    
# Print the type of ent
print(type(ent))

# Initialize the count variable: count
count = 0

# Iterate over all the entities
for ent in txt.entities:
    # Check whether the entity contains 'Márquez' or 'Gabo'
    if "Márquez" in ent or "Gabo" in ent:
        # Increment count
        count += 1

# Print count
print(count)

# Calculate the percentage of entities that refer to "Gabo": percentage
percentage = count / len(txt.entities)
print(percentage)
