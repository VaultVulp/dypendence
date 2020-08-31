import logging

import pytest
from loguru import logger


@pytest.fixture(name='caplog', autouse=True)
def loguru_caplog(caplog):

    class PropogateHandler(logging.Handler):

        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    logger.remove()
    handler_id = logger.add(PropogateHandler(), format='{message}', backtrace=False)
    caplog.clear()
    yield caplog
    logger.remove(handler_id)
