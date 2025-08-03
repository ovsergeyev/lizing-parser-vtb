from pydantic import BaseModel, field_validator
from typing import Optional


class VTBAuto(BaseModel):
    slug: str
    title: str
    image_url: str
    year_of_release: int
    mileage: int
    location: str
    vin: str
    price: int
    old_price: Optional[int] = None
    offer_code: str

    @field_validator("price", mode="before")
    def parse_price(cls, v):
        if isinstance(v, str):
            res = v.replace("от", "")
            res = res.replace("₽", "")
            res = "".join(res.split())
            return int(res)
        return v

    @field_validator("mileage", mode="before")
    def parse_mileage(cls, v):
        if isinstance(v, str):
            try:
                res = "".join(v.split())
                return int(res)
            except:
                return -1
        return v
