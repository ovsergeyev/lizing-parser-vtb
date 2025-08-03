from typing import Any, Optional

from sqlalchemy import select

from core.db.database import async_session
from core.db.models.vtb_auto import VTBAuto


class VTBAutoDAO:
    @staticmethod
    async def create(vtb_auto: dict[str, Any]) -> VTBAuto:
        async with async_session() as session:
            async with session.begin():
                db_vtb_auto = VTBAuto(**vtb_auto)
                session.add(db_vtb_auto)
            await session.commit()
            return db_vtb_auto

    @staticmethod
    async def exists_by_slug(slug: str) -> bool:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(VTBAuto).where(VTBAuto.slug == slug))
                return bool(result.scalars().first())

    @staticmethod
    async def get_price_by_slug(slug: str) -> Optional[int]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(VTBAuto.price).where(VTBAuto.slug == slug))
                db_vtb_auto = result.scalars().first()
                if db_vtb_auto:
                    return db_vtb_auto
                return None

    @staticmethod
    async def update(vtb_auto: dict[str, Any]) -> Optional[VTBAuto]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(VTBAuto).where(VTBAuto.slug == vtb_auto["slug"]))
                db_vtb_auto = result.scalars().first()
                if db_vtb_auto:
                    for key, value in vtb_auto.items():
                        setattr(db_vtb_auto, key, value)
                await session.commit()
                return db_vtb_auto
