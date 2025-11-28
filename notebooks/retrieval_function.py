import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import requests
import detectlanguage

languages = ['en', 'es', 'fr', 'de', 'it', 'ru', 'zh-CN', 'iw'] # list of languages used
NGRAM_API_URL = "https://books.google.com/ngrams/json" # API endpoint
detectlanguage.configuration.api_key = "2f804e5b6f76b1bacb52d2ad6667f374" # personal API key for detectlanguage service

# sets parameters for API call
def set_params(word, corpus):
    params = {'content': word,
              'year_start': 1500,
              'year_end': 2022,
              'corpus': corpus,
              'smoothing': 0,
              'case_insensitive': 'on'}
    return params

# function to get direct translations for words
def get_languages(input, input_lang):
    df = pd.DataFrame({'word' : input,
                       'language' : input_lang}, index = [0])
    for lang in languages:
        if lang != input_lang:
            translator = GoogleTranslator(source = input_lang, target = lang)
            new_entry = pd.DataFrame({'word' : translator.translate(input),
                            'language' : lang}, index = [0])
            df = pd.concat([df, new_entry], ignore_index = True)
            df['language'] = df['language'].replace('zh-CN', 'zh')
    return df

# gets frequency data from google ngram API
def get_frequency(df):
    years = list(range(1500, 2023))
    data = pd.DataFrame()
    for i in range(len(df)):
        response = requests.get(NGRAM_API_URL, params = set_params(df['word'][i], df['language'][i],), timeout = 30)
        if response.status_code == 200:
            x = response.json()
            if x:
                freq = x[0]['timeseries']
            else:
                freq = [0] * len(years)
        else:
            freq = [0] * len(years)
        data = pd.concat([data, pd.DataFrame({'word': df['word'][i], 
                                              'language' : df['language'][i],
                                              'year' : years, 
                                              'frequency' : freq})], ignore_index = True)
    return data

# main function to run (combines above functions)
def get_df(word, input_lang):
    return get_frequency(get_languages(word, input_lang))

# detect language of input word usage
def detect_language(word):
    return detectlanguage.detect_code(word)