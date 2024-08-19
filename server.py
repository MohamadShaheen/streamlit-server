import os
import logging
from fastapi import FastAPI
from routers import baby_names_router

if not os.path.exists('logs'):
    os.mkdir('logs')
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='[%d-%m-%Y] (%H:%M:%S)',
    force=True
)

app = FastAPI()

app.include_router(baby_names_router.router, prefix='/baby-names', tags=['Baby Names'])
