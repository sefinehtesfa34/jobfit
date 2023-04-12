import pandas as pd 
import numpy as np 
import re 
from nltk.corpus import stopwords
df = pd.read_csv('backend/recommender/resume.csv')
print(df.head(5))
