import requests
import pandas as pd
import json
"""Classifier Part"""
# Will do later.
"""Topic Modelling Part"""
# /api/topic_models post

# data = {
#     "topic_model_name": "all things must pass", "num_topics": 10, 
#     "notify_at_email": "vibs97@bu.edu", "language": "french",
#     "remove_stopwords": True, "remove_punctuation": True, 
#     "do_stemming": False, "do_lemmatizing": False
#     }
# res = requests.post('http://localhost:5000/api/topic_models/', json=data)
# print(res.text)


# api/topic_models/1 get
"""
res = requests.get('http://0.0.0.0:5000/api/topic_models/1')
print(res.text)
"""

# api/topic_models/1/training/file/

fil = open('testing_files/train_fr.csv', 'r')
data = {"file": fil} 
# print(pd.read_csv(fil))
res = requests.post('http://0.0.0.0:5000/api/topic_models/10/training/file', files=data)
print(res.text)


# api/topic_models/1/topics/preview get
"""
res = requests.get('http://0.0.0.0:5000/api/topic_models/1/topics/preview')
print(res.text)
"""

# api/topic_models/1/topics/keywords get
# api/topic_models/1/topics_by_doc get
"""
# This is an excel file so won't be used here but in browser, you can download this.
res = requests.get('http://0.0.0.0:5000/api/topic_models/1/keywords?file_type=xlsx')
print(pd.read_excel(res.raw))
"""

# /topic_models/1/topics/names
"""
data = {"topic_names": ['my', 'name', 'is', 'vubh', '5', '6', '7', '8', '9', '10']}
res = requests.post('http://0.0.0.0:5000/api/topic_models/1/topics/names', json=data)
print(res.text)
"""
