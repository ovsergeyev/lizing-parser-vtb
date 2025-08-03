import re
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from core.db.vtb_auto_dao import VTBAutoDAO
from core.schemas.vtb_auto_schema import VTBAuto
from core.utils.tg_bot import TgBot
from logger import get_logger
from settings import settings

logger = get_logger("app")


def get_subling_element_text(parent_element: WebElement, text: str) -> str:
    result = ""
    try:
        element = parent_element.find_element(
            By.XPATH,
            f".//div[@class='t-tab-content-column-item']/div[contains(., '{text}')]/following-sibling::*[1]",
        )
        result = element.text.strip()
    except Exception as e:
        logger.debug(f"Произошла ошибка в get_subling_element_text: {e}")
    return result


def get_link_from_background(element: WebElement) -> str:
    image_url = ""
    try:
        bg_value = element.value_of_css_property("background-image")
        match = re.search(r'url\("?(.*?)"?\)', bg_value)
        if match:
            image_url = match.group(1)
        else:
            logger.error("Не найдена ссылка на изображение в background-image")

        return image_url
    except Exception as e:
        logger.debug(f"Произошла ошибка в get_link_from_background: {e}")
    return image_url


async def parse_pages(driver: WebDriver, tg_bot: TgBot):
    logger.debug("Запуск parse_pages")

    try:
        slug = driver.current_url.split("/")[5]
        title = driver.find_element(By.XPATH, "//h1").text
        image_div = driver.find_element(By.XPATH, "//div[@open-popup-gallery='true' and @data-swiper-slide-index='0']")
        image_url = get_link_from_background(image_div)

        parrent_element = driver.find_element(By.XPATH, "//div[@class='t-auto-card-info']")
        year_of_release = get_subling_element_text(parrent_element, "Год выпуска")
        mileage = get_subling_element_text(parrent_element, "Пробег")
        location = get_subling_element_text(parrent_element, "Город")
        vin = get_subling_element_text(parrent_element, "VIN")
        offer_code = get_subling_element_text(parrent_element, "Код предложения")

        price = 0
        price_element = driver.find_element(By.XPATH, "//div[@class='t-calculator-card-price']")
        if price_element:
            price = price_element.text.strip()

        avto = VTBAuto(
            slug=slug,
            title=title,
            image_url=image_url,
            year_of_release=year_of_release,  # type: ignore
            mileage=mileage,  # type: ignore
            location=location,
            vin=vin,
            price=price,  # type: ignore
            offer_code=offer_code,
        )

        logger.debug(f"Добавляем {avto=}")

        if await VTBAutoDAO.exists_by_slug(slug):
            old_price = await VTBAutoDAO.get_price_by_slug(slug)
            if old_price != avto.price:
                avto.old_price = old_price
                await tg_bot.send_message(avto)
                await VTBAutoDAO.update(avto.model_dump(exclude={"old_price"}))
            pass
        else:
            if settings.mode != "deployment":
                await tg_bot.send_message(avto)

            await VTBAutoDAO.create(avto.model_dump(exclude={"old_price"}))

    except Exception as e:
        logger.debug(f"Произошла ошибка в parse_pages: {e}")


async def crawler_pages(driver: WebDriver, links: list[str]):
    logger.debug("Запуск crawler_pages")
    tg_bot = TgBot()

    for link in links:
        try:
            if not link:
                break

            driver.get(link)
            await parse_pages(driver, tg_bot)
            # sleep(100)

        except Exception as e:
            logger.debug(f"Произошла ошибка в crawler_pages: {e}")
