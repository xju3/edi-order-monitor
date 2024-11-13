import logging
from datetime import datetime


def init_logger(log_name, file_name):
    now = datetime.now()
    file_name = file_name.format(now.strftime('%Y%m%d%H%M%S'))
    logging.basicConfig(filename=file_name,
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
