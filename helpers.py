# Usefull functions for NLP
import pandas as pd
import emoji
import unidecode
import string
import re

def clean_tweets(data:pd.DataFrame):
    data['clean_text'] = data['text'].apply(lambda x: emoji.demojize(x, delimiters=(" ", " ")))
    data['clean_text'] = data['clean_text'].apply(lambda x: unidecode.unidecode(x))
    data['clean_text'] = data['clean_text'].str.replace('\d+', '')
    data['clean_text'] = data['clean_text'].apply(lambda s :s.translate(str.maketrans('', '', string.punctuation)))
    data['clean_text'] = data['clean_text'].apply(lambda x:re.sub(r'http\S+', '', x))

    return(data)