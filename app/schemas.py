from pydantic import BaseModel
from datetime import date


class StockCreate(BaseModel):
    symbol: str
    company_name: str
    sector: str


class PriceCreate(BaseModel):
    stock_symbol: str
    date: date
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int