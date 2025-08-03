from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from logger import get_logger

logger = get_logger("app")


def get_driver() -> WebDriver:
    service = Service(ChromeDriverManager().install(), verbose=True)
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")

    # Log Options
    # options.add_argument("--enable-logging=stderr")
    # options.add_argument("--v=1")

    # For docker options
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Anonimus options
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.85 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(60)
    return driver
