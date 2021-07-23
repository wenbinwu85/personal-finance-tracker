import logging
from .cjs import CJS

logger = logging.getLogger('ahben')
logger.setLevel('DEBUG')
# handler = logging.FileHandler('./finman.log')
# formatter = logging.Formatter('%(asctime)s : %(filename)s.%(funcName)s : %(levelname)s : %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


def load_data(file):
    """"""
    return CJS().load(file)


def dump_data(data, file):
    """"""
    CJS().dump(data, file)
