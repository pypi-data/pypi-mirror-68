import logging
from typing import Callable, Dict

import ssl
import urllib.request
import urllib.error
import time

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

__all__ = ['get_soup', 'PARSER_DICT', 'parser_decorator', 'BeautifulSoup']


def get_soup(url: str, num_of_attempts: int = 3, delay: float = 1.) -> BeautifulSoup or None:
    if num_of_attempts == -1:
        return
    try:
        html = urllib.request.urlopen(url, context=_get_context()).read()
        logger.debug(f'Successfully parsed url.')
        return BeautifulSoup(html, 'html.parser')
    except Exception as err:
        logger.exception(err)
        logger.info(f'Another try in {delay} sec. Number of attempts remained: {num_of_attempts}.')
        time.sleep(delay)
        return get_soup(url, num_of_attempts - 1, delay * 2)


def _get_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def parser_decorator(url: str):
    def dec(func):

        def wrapper(*args, **kwargs):
            soup = get_soup(url, *args, **kwargs)
            if soup:
                return func(soup)
            else:
                logger.error(f'Parser returned NoneType object.')
                return

        setattr(wrapper, 'url', url)
        return wrapper

    return dec


PARSER_DICT: Dict[str, Callable] = {}
