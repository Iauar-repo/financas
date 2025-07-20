import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'app.log')

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S'
    )

    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    stream.setLevel(logging.DEBUG if app.debug else logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(stream)

    app.logger = logger

    # Silence werkzeug and other loggers
    #logging.getLogger('werkzeug').disabled = True
    #logging.getLogger().handlers.clear()  # clean root logger
