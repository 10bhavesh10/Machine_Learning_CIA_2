import numpy as np
import pandas as pd
import re

df=pd.read_csv('reviews_feb_2023.csv')

df.drop(['with_milk','acidity_structure','bottom_line'],axis=1,inplace=True)

df['aftertaste'].fillna(df['aftertaste'].median(),inplace=True)

df.fillna(method='bfill',inplace=True)

df['coffee_origin'].fillna(method='ffill',inplace=True)
df['est_price'].fillna(method='bfill',inplace=True)

df.drop('est_price',axis=1,inplace=True)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf=TfidfVectorizer()

tfidf_mat=tfidf.fit_transform(df['blind_assessment'])

from sklearn.metrics.pairwise import linear_kernel

cosine_sim=linear_kernel(tfidf_mat,tfidf_mat)

df1=pd.DataFrame(pd.Series(df['blind_assessment'],index=df.index))

class Recommendation:
    def __init__(self):
        self.df1=df1
        self.cosine_sim=cosine_sim
    def recommendation(self,x,a):
        ind=self.df1[df1['blind_assessment'].str.contains(x,flags=re.IGNORECASE,regex=True)].index[0]
        sim_score=list(enumerate(self.cosine_sim[ind]))
        sim_score=sorted(sim_score,key=lambda a:a[1],reverse=True)
        sim_score=sim_score[1:a+1]
        final_ind=[i[0] for i in sim_score]
        return final_ind
    def predict(self,x,a):
        l1=pd.DataFrame()
        ind=self.recommendation(x,a)
        l1['title']=df['title'].iloc[ind]
        l1['rating']=df['rating'].iloc[ind]
        l1['url']=df['url'].iloc[ind]
        return l1
        
        


import pickle
rec=Recommendation()
pickle.dump(rec,open('model.pkl','wb'))

