import requests
import pandas as pd
import json
from numpy import fromfile

"""Classifier Part"""
# /api/classifiers post
"""
category_names = ['Politics', '2nd Amendment rights', 'Gun control', 
    'Public opinion', 'Mental health', 'School or public space safety', 
    'Society', 'Race', 'Economic consequences']

data = {
    "name": "sample classifier", "notify_at_email": "vibs97@bu.edu",
    "category_names": category_names
    }
res = requests.post('http://localhost:5000/api/classifiers/', json=data)
print(res.text)
"""

# /api/classifiers/1 get
"""
res = requests.get('http://localhost:5000/api/classifiers/1')
print(res.text)
"""

# /api/classifiers/1/training/file post
""" 
fil = open('testing_files/train_classifier.csv', 'r')
data = {"file": fil}
res = requests.post('http://0.0.0.0:5000/api/classifiers/1/training/file', files=data)
print(res.text)
"""

# /api/classifiers/1/test_sets post
"""
data = {
    "test_set_name": "sample classifier_training_Set2", "notify_at_email": "vibs97@bu.edu"
}
res = requests.post('http://0.0.0.0:5000/api/classifiers/1/test_sets/', json=data)
print(res.text)
"""

# /api/classifiers/1/test_sets get
"""
res = requests.get('http://0.0.0.0:5000/api/classifiers/7/test_sets')
print(res.text)
"""

# /api/classifiers/1/test_sets/1/file/ get
"""
fil = open('testing_files/test_classifier.csv', 'r')
data = {"file": fil}
res = requests.post('http://0.0.0.0:5000/api/classifiers/1/test_sets/2/file',files=data)
print(res.text)
"""

# /api/classifiers/1/test_sets/1/predictions get
"""
res = requests.get('http://0.0.0.0:5000/api/classifiers/7/test_sets/1/predictions')
"""


"""Topic Modelling Part"""
# /api/topic_models post
"""
data = {
    "topic_model_name": "all things must pass", "num_topics": 10, 
    "notify_at_email": "vibs97@bu.edu", "language": "french",
    "remove_stopwords": True, "remove_punctuation": True, 
    "do_stemming": False, "do_lemmatizing": False
    }
res = requests.post('http://localhost:5000/api/topic_models/', json=data)
print(res.text)
"""

# api/topic_models/1 get
"""
res = requests.get('http://0.0.0.0:5000/api/topic_models/1')
print(res.text)
"""

# api/topic_models/1/training/file/

"""
fil = open('testing_files/train_fr.csv', 'r')
data = {"file": fil} 
# print(pd.read_csv(fil))
res = requests.post('http://0.0.0.0:5000/api/topic_models/10/training/file', files=data)
print(res.text)
"""

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
