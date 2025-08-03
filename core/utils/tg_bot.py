import asyncio

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile

from core.schemas.vtb_auto_schema import VTBAuto
from settings import settings

# from fake_useragent import UserAgent


class TgBot:
    def __init__(self):
        self.bot = Bot(token=settings.bot.token)
        self.chat_id = settings.bot.chat_id
        # self.ua = UserAgent(browsers=["chrome"])

    async def send_message(self, auto: VTBAuto):
        # headers = {"user-agent": self.ua.random}
        headers = {}

        image_from_url = URLInputFile(auto.image_url, headers=headers) if auto.image_url else None
        price_formatted = f"{auto.price:,}".replace(",", " ")

        caption_lines = [
            f"<b>VTB ЛИЗИНГ: {auto.title}</b>\n\r",
        ]

        if getattr(auto, "year_of_release", None):
            caption_lines.append(f"<b>Год выпуска:</b> <code>{auto.year_of_release}</code>")

        if getattr(auto, "mileage", None):
            mileage_formatted = f"{auto.mileage:,}".replace(",", " ")
            caption_lines.append(f"<b>Пробег:</b> <code>{mileage_formatted} км.</code>")

        if getattr(auto, "vin", None):
            caption_lines.append(f"<b>VIN:</b> <code>{auto.vin}</code>")

        caption_lines.append(f"<b>Адрес:</b> <code>{auto.location}</code>")

        if getattr(auto, "offer_code", None):
            caption_lines.append(f"<b>Код предложения:</b> <code>{auto.offer_code}</code>")

        if getattr(auto, "old_price", None):
            old_price_formatted = f"{auto.old_price:,}".replace(",", " ")
            caption_lines.append(f"<b>Старая цена:</b> <s>{old_price_formatted} ₽</s>")

        caption_lines.append(f"<b>Цена:</b> <code>{price_formatted} ₽</code> \n\r")
        caption_lines.append(f"<a href='https://www.vtb-leasing.ru/auto/probeg/{auto.slug}/'>Ссылка</a>")

        caption = "\n\r".join(caption_lines)

        if image_from_url:
            await self.bot.send_photo(chat_id=self.chat_id, photo=image_from_url, caption=caption, parse_mode="HTML")
            await asyncio.sleep(2)
