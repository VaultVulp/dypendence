import sys

from dynaconf import settings
from loguru import logger


async def setup_logger() -> None:
    logger.remove()
    if settings.IS_DEBUG:
        level = 'DEBUG'
        diagnose = True
    else:
        level = 'INFO'
        diagnose = False
    logger.add(
        sys.stdout,
        level=level,
        diagnose=diagnose,
    )
