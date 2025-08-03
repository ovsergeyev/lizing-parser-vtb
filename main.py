import asyncio

from core.utils.get_driver import get_driver
from core.utils.crawler_pagination import crawler_pagination

from core.utils.crawler_pages import crawler_pages


BASE_URL = "https://www.vtb-leasing.ru/truck/"
from logger import get_logger, clear_log, setup_logging

# clear_log()
setup_logging()
logger = get_logger("app")


async def run():
    logger.info("=================START=================")
    logger.info("=======================================")
    logger.info("=======================================")
    try:
        driver = get_driver()
        driver.get(BASE_URL)

        links: list[str] = await crawler_pagination(driver, limit=0)

        await crawler_pages(driver, links)

    except Exception as e:
        logger.error(f"Непредвиденная ошибка {e}")
    logger.info("==================END==================")


if __name__ == "__main__":
    asyncio.run(run())
