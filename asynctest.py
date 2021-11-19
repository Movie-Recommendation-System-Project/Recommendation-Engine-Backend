from pandas.io import api
from aiohttp import ClientSession
import os
import json
import asyncio
import aiohttp
import time


startt = time.time()
print("asyc")
API_KEY = "99559c6f0e7066b79de89be2945150ec"


MOVIEDB_URL = "https://api.themoviedb.org/3/movie/"


LIST_ISBN = []
api_response = {}


def extract_fields_from_response(response):
    """Extract fields from API's response"""
    # extract backdrop_path, genres, id, original title,
    # overview, poster_path, popularity, tagline, vote_average from response
    backdrop_path = response.get('backdrop_path')
    genres = response.get('genres')
    id = response.get('id')
    original_title = response.get('original_title')
    overview = response.get('overview')
    poster_path = response.get('poster_path')
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


async def get_book_details_async(isbn, session):
    url = MOVIEDB_URL + str(isbn)+"?api_key="+API_KEY
    try:
        response = await session.request(method='GET', url=url)
        response.raise_for_status()
        print(f"Response status ({url}): {response.status}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    response_json = await response.json()
    return response_json


async def run_program(isbn, session):
    """Wrapper for running program in an asynchronous manner"""
    try:
        response = await get_book_details_async(isbn, session)
        parsed_response = extract_fields_from_response(response)
        api_response[isbn] = parsed_response
        #print(f"Movie: {json.dumps(parsed_response, indent=2)}")

    except Exception as err:
        print(f"Exception occured: {err}")
        pass


async def main():
    async with ClientSession() as session:
        await asyncio.gather(*[run_program(isbn, session) for isbn in LIST_ISBN])


def start(movie_list):
    global LIST_ISBN
    LIST_ISBN = movie_list
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    return api_response
    # asyncio.run(main())
