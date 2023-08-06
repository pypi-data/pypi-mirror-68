import time
import sys
import logging
import logging.config
import json
from pathlib import Path

from .config import Config
from .parser import (PARSER_DICT,
                     parser_decorator,
                     BeautifulSoup)
from .config_cmd import ConfigCmd
from .main import FindHome

import traceback

__all__ = ['main_loop', 'test_urls', 'BeautifulSoup', 'edit_config', 'parser_decorator', 'PARSER_DICT']


def excepthook(excType, excValue, tracebackobj):
    """
    Log all the uncaught errors.
    """

    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    logging.error(errmsg)
    logging.error(''.join(traceback.format_tb(tracebackobj)))


def setup_logging(path: str or Path = 'logging.json'):
    if isinstance(path, str):
        path = Path(__file__).parent / path
    with open(path, 'rt') as f:
        log_dict = json.load(f)
        logging.config.dictConfig(log_dict)


def main_loop(config_path: str = None, *, delay: int = None):
    setup_logging()
    fh = FindHome(config_path)
    delay = delay or fh.config.delay
    while True:
        time.sleep(delay)
        fh.check()


def test_urls():
    for k, func in PARSER_DICT.items():
        try:
            print(k, ', url: ', func.url)
            print('Result: ', func())
        except Exception as err:
            print(f'Exception occurred for {k}', err)


def edit_config():
    setup_logging()
    sys.excepthook = excepthook
    ConfigCmd().cmdloop()
