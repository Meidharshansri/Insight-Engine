from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, Numeric, BigInteger, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

# Define Base FIRST
Base = declarative_base()


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())

    prices = relationship("HistoricalPrice", back_populates="stock")


class HistoricalPrice(Base):
    __tablename__ = "historical_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    open_price = Column(Numeric(10, 2))
    close_price = Column(Numeric(10, 2))
    high_price = Column(Numeric(10, 2))
    low_price = Column(Numeric(10, 2))
    volume = Column(BigInteger)
    created_at = Column(TIMESTAMP, server_default=func.now())

    stock = relationship("Stock", back_populates="prices")