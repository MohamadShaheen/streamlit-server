import logging
from fastapi import APIRouter, Request
from data_access_layer import currencies_dal

router = APIRouter()

@router.post('/store-currencies/')
async def store_currencies(request: Request):
    logging.info(f'Accessing {request.url}')

    try:
        currencies = currencies_dal.store_currencies()
        logging.info('Currencies stored')
        return currencies
    except Exception as e:
        logging.error(e)
        raise e

@router.get('/retrieve-all-currencies/')
async def retrieve_all_currencies(request: Request):
    logging.info(f'Accessing {request.url}')

    try:
        currencies = currencies_dal.retrieve_all_currencies()
        logging.info('Currencies retrieved')
        return currencies
    except Exception as e:
        logging.error(e)
        raise e

@router.get('/convert-currencies/')
async def convert_currencies(request: Request, from_currency: str, to_currency: str, amount: float):
    logging.info(f'Accessing {request.url}')

    try:
        conversion_result = currencies_dal.convert_currencies(from_currency, to_currency, amount)
        logging.info('Currencies converted')
        return conversion_result
    except Exception as e:
        logging.error(e)
        raise e
