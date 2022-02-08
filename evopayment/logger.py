import logging

from .settings import settings


def logger_init() -> None:
    """ Logger initialization """
    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s [%(filename)s:%(lineno)s] %(message)s')

    # StreamHandler
    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(settings.log_level.upper())
    handler_stream.setFormatter(formatter)

    # Logger
    logging.getLogger().setLevel(logging.ERROR)

    for name in ['fastapi', 'uvicorn', 'uvicorn.access', 'uvicorn.error', 'tornado.access']:
        logging.getLogger(name).setLevel(logging.ERROR)

    logger = logging.getLogger('iperon')
    logger.addHandler(handler_stream)
    logger.setLevel(settings.log_level.upper())

    logger_db_client = logging.getLogger('db_client')
    logger_db_client.addHandler(handler_stream)
    logger_db_client.setLevel(settings.log_level.upper())
