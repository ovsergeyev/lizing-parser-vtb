from selenium.webdriver.chrome.webdriver import WebDriver
from core.utils.pagination import Pagination
from logger import get_logger
from selenium.webdriver.common.by import By

logger = get_logger("app")

pagination_link_xpath = "//a[contains(@onclick, 'showMarketPage') and not(contains(@href, 'javascript:void'))]"
link_xpath = "//a[contains(., 'Подробнее') and contains(@href, '/auto/')]"


def save_pagination_links(driver: WebDriver, pagination: Pagination):
    link_tags = driver.find_elements(By.XPATH, pagination_link_xpath)
    links = [link.get_attribute("href") for link in link_tags]
    pagination.add_links(links)


def parse_links(driver: WebDriver):
    link_tags = driver.find_elements(By.XPATH, link_xpath)
    links = [link.get_attribute("href") for link in link_tags if link.get_attribute("href")]
    return links


async def crawler_pagination(driver: WebDriver, limit: int = 0) -> list[str]:
    logger.debug("Запуск crawler_pagination")

    pagination = Pagination()

    save_pagination_links(driver, pagination)

    counter = 0
    result = []
    try:
        while True:
            if limit and counter >= limit:
                break
            counter += 1

            link = pagination.get_link()
            if not link:
                break

            logger.debug(f"Переход на страницу {link}")
            driver.get(link)

            save_pagination_links(driver, pagination)

            result += parse_links(driver)
        logger.debug(f"Обошли {counter} ссылок пагинации")
    except Exception as e:
        logger.debug(f"Произошла ошибка в crawler_pagination: {e}")
    return result
