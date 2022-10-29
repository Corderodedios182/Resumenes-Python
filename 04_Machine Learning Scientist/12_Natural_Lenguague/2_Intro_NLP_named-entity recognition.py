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

corpus = str(pd.read_parquet(path = "raw/búsquedas_con_retro_recortado.parquet").loc[:,"TEXTO_COMPARACION"].unique()).replace("]", "").replace("[", "").replace("'", "").replace("\n", "")

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
