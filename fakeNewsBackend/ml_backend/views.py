from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
import gensim
from tensorflow.keras.preprocessing.text import  Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

df = pd.read_csv('./ml_backend/data/fakereal.csv')
nltk.download('stopwords')
stop_words = stopwords.words("english")

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3 and token not in stop_words:
            result.append(token)
            
    return result

list_of_words = []
for i in df.clean:
    for j in i:
        list_of_words.append(j)

total_words = len(list(set(list_of_words)))

df['clean_joined'] = df['clean'].apply(lambda x: " ".join(x))

tokenizer = Tokenizer(num_words = total_words)
tokenizer.fit_on_texts(df.clean)

#Model
model=tf.keras.models.load_model('./ml_backend/model')

def get_label(text,tokenizer):
    processed = tokenizer.texts_to_sequences([" ".join(text)])
    processed = pad_sequences(processed,maxlen = 40, padding = 'post', truncating = 'post')
    return processed


class Get_predictions(APIView):
    def post(self, request, *args, **kwargs):
        text = self.request.data["text_string"]
        text = preprocess(text)
        text = get_label(text, tokenizer)
        temp = model.predict(text)[0][0]
        if temp>0.9:
            out=1
        else:
            out=0
        return JsonResponse({
                "message": out,
                "status": True,
            })
