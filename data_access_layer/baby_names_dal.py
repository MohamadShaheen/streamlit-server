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
        if len(baby_names_to_insert) > 0:
            collection.insert_many(baby_names_to_insert)

        return baby_names
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

def retrieve_baby_names(gender: str = None, num_of_baby_names: int = None):
    gender = gender.lower()
    if gender == 'both':
        gender = None

    if gender:
        if gender != 'boy' and gender != 'girl':
            raise HTTPException(status_code=400, detail="Gender must be 'boy' or 'girl'")
        db_baby_names = collection.find({'gender': gender}, {'_id': 0, 'gender': 0})
    else:
        db_baby_names = collection.find({}, {'_id': 0, 'gender': 0})

    if not db_baby_names:
        raise HTTPException(status_code=404, detail='No baby names found')

    baby_names_list = [db_baby_name['baby_name'] for db_baby_name in db_baby_names]
    if num_of_baby_names:
        if num_of_baby_names == 0 or len(baby_names_list) < num_of_baby_names:
            return baby_names_list
        else:
            return random.sample(baby_names_list, num_of_baby_names)
    else:
        if len(baby_names_list) < 300:
            return baby_names_list
        else:
            return random.sample(baby_names_list, 300)
