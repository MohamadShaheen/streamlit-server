import random
import requests
from fastapi import HTTPException
from api_keys import ninjas_api_key
from mongodb_connection import client

database = client['ninjas_database']
collection = database['baby_names']
api_url = 'https://api.api-ninjas.com/v1/babynames'

def store_baby_names():
    gender = random.choice(['boy', 'girl'])
    params = {'gender': gender}
    headers = {'X-Api-Key': ninjas_api_key}
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == requests.codes.ok:
        baby_names = response.json()

        existing_baby_names = collection.find({'gender': gender}, {'_id': 0, 'gender': 0})
        existing_baby_names_set = set(baby_name['baby_name'] for baby_name in existing_baby_names)

        baby_names_to_insert = []
        for baby_name in baby_names:
            if baby_name not in existing_baby_names_set:
                baby_names_to_insert.append({
                    'baby_name': baby_name,
                    'gender': gender
                })
        collection.insert_many(baby_names_to_insert)

        return baby_names
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
