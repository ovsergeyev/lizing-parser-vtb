from sqlalchemy import Column, Integer, String

from core.db.database import Base


class VTBAuto(Base):
    __tablename__ = "vtb_auto"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, index=True)
    title = Column(String)
    image_url = Column(String)
    year_of_release = Column(Integer)
    mileage = Column(Integer)
    location = Column(String)
    vin = Column(String)
    price = Column(Integer)
    offer_code = Column(String)
