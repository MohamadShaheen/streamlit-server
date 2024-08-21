import logging
from fastapi import APIRouter, Request
from data_access_layer import baby_names_dal

router = APIRouter()

@router.post('/store-baby-names/')
async def store_baby_names(request: Request):
    logging.info(f'Accessing {request.url}')

    try:
        baby_names = baby_names_dal.store_baby_names()
        logging.info('Baby names stored')
        return baby_names
    except Exception as e:
        logging.error(e)
        raise e

@router.get('/retrieve-baby-names/')
async def retrieve_baby_names(request: Request, gender: str = None, num_of_baby_names: int = None):
    logging.info(f'Accessing {request.url}')
    try:
        baby_names = baby_names_dal.retrieve_baby_names(gender, num_of_baby_names)
        logging.info('Baby names retrieved')
        return baby_names
    except Exception as e:
        logging.error(e)
        raise e
