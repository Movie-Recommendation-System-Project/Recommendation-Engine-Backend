import os
import json
import requests
from requests.exceptions import HTTPError

import time


startt = time.time()
API_KEY = "99559c6f0e7066b79de89be2945150ec"


MOVIEDB_URL = "https://api.themoviedb.org/3/movie/"


LIST_ISBN = []
api_response = {}


def extract_fields_from_response(response):
    # extract backdrop_path, genres, id, original title,
    # overview, poster_path, popularity, tagline, vote_average from response
    backdrop_path = "https://image.tmdb.org/t/p/w500" + \
        response.get('backdrop_path')
    genres = response.get('genres')
    id = response.get('id')
    original_title = response.get('original_title')
    overview = response.get('overview')
    poster_path = "https://image.tmdb.org/t/p/w500"+response.get('poster_path')
    popularity = response.get('popularity')
    tagline = response.get('tagline')
    vote_average = response.get('vote_average')
    return {
        'original_title': original_title,
        'overview': overview,
        'tagline': tagline,
        'genres': genres,
        'poster_path': poster_path,
        'popularity': popularity,
        'vote_average': vote_average,
        'backdrop_path': backdrop_path
    }


def get_book_details_seq(isbn, session):
    url = MOVIEDB_URL + str(isbn)+"?api_key="+API_KEY
    response = None
    try:
        response = session.get(url)
        response.raise_for_status()
        print(f"Response status ({url}): {response.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    response_json = response.json()
    return response_json


def start(movie_list):
    global LIST_ISBN
    LIST_ISBN = movie_list
    print(f"List of ISBNs: {LIST_ISBN}")

    with requests.Session() as session:
        api_response.clear()
        for isbn in LIST_ISBN:
            try:
                response = get_book_details_seq(isbn, session)
                parsed_response = extract_fields_from_response(response)
                api_response[isbn] = parsed_response
                #print(f"Response: {json.dumps(parsed_response, indent=2)}")
            except Exception as err:
                print(f"Exception occured: {err}")
                pass
    return api_response
