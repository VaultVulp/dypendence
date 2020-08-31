import asyncio

import click
from loguru import logger

from dypendence.logger import setup_logger


@click.group()
def cli():
    pass


@cli.command()
def main():
    try:
        asyncio.run(setup_logger())
        logger.info('Starting Dypendence ...')
        asyncio.run(do_work())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Closing Dypendence')
    except Exception:
        logger.exception('Critical Error!')


async def do_work():
    await asyncio.sleep(3)
    logger.info("Job's Done!")
