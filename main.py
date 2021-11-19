from pandas.io import api
from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from nonasync import *
from typing import List, Optional
from pydantic import BaseModel


# import library for http requests

class Item(BaseModel):
    movieIds: List[str]


app = FastAPI()

df1 = pd.read_csv("movies.csv")
cosine_sim = pickle.load(open('similarity.pkl', 'rb'))
df1.drop("Unnamed: 0", axis=1, inplace=True)


def recommend(movie_id):
    dict = {}
    movie_list = []
    x = 0
    index = df1[df1['movie_id'] == int(movie_id)].index[0]
    distances = sorted(
        list(enumerate(cosine_sim[index])), reverse=True, key=lambda x: x[1])
    for i in distances:
        # extract movie_id from distance
        movie_list.append(int(df1.iloc[i[0]]['movie_id']))
        # remove first element from the list
        if x == 0:
            movie_list.pop(0)
        x = x+1
        if x > 10:
            break
    api_response = start(movie_list)
    return api_response


@app.get("/")
async def read_root():

    random_five = df1.sample(6)
    # convert movie_id from random_five to list
    list_of_movie_id = random_five['movie_id'].tolist()
    # convert list of movie_id to list of movie_name
    list_of_movie_name = []
    for i in list_of_movie_id:
        list_of_movie_name.append(df1.loc[(df1['movie_id'] == i)].values[0][1])
    # make a dictionary with key as movie title and value as movie_id
    dict_of_movie_id = {}
    for i in range(len(list_of_movie_name)):
        dict_of_movie_id[list_of_movie_name[i]] = list_of_movie_id[i]
    print(type(list_of_movie_id))
    api_response = start(list_of_movie_id)

    return api_response


@app.get("/movie_id/{movie_id}")
async def read_item(movie_id: str):
    return recommend(movie_id)


@app.post("/favorites/")
async def get_movie_ids(item: Item):
    list_of_movie_id = item.movieIds
    api_response = start(list_of_movie_id)
    return api_response
