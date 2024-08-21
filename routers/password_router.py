import logging
import secrets
import string

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

SYMBOLS = '!@#$%^&*()+'
EXTRA_SYMBOLS = '~`[];?,'

@router.get('/')
async def generate_password(request: Request, length: int = 20, allow_numbers: bool = True,
                            allow_lowercase: bool = True, allow_uppercase: bool = True,
                            allow_symbols: bool = True, allow_extra_symbols: bool = False):
    logging.info(f'Accessing {request.url}')

    allowed_chars = ''

    if allow_numbers:
        allowed_chars += string.digits
    if allow_lowercase:
        allowed_chars += string.ascii_lowercase
    if allow_uppercase:
        allowed_chars += string.ascii_uppercase
    if allow_symbols:
        allowed_chars += SYMBOLS
    if allow_extra_symbols:
        allowed_chars += EXTRA_SYMBOLS

    if allowed_chars == '':
        raise HTTPException(status_code=400, detail='Unable to create password because no characters were allowed')

    password = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    return password
