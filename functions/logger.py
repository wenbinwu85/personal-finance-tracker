import logging

logger = logging.getLogger('finman')
logger.setLevel('DEBUG')
# handler = logging.FileHandler('./finman.log')
# formatter = logging.Formatter('%(asctime)s : %(filename)s.%(funcName)s : %(levelname)s : %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


if __name__ == '__main__':
    logger.debug('this is a bug')
    logger.info('this is some info')
    logger.warning('This is a warning.')
    
    name = 'module x'
    logger.error('oops, something went wrong with %s!', name)

    try:
        5/0
    except ZeroDivisionError:
        logger.exception('Oops! Got an exception:')
