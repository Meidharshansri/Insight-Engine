import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Stock, HistoricalPrice
from app.schemas import StockCreate, PriceCreate


# -------------------------
# Database Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Router
# -------------------------
router = APIRouter()


# -------------------------
# CREATE STOCK
# -------------------------
@router.post("/stocks")
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):

    existing_stock = db.query(Stock).filter(Stock.symbol == stock.symbol).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail="Stock already exists")

    new_stock = Stock(
        symbol=stock.symbol,
        company_name=stock.company_name,
        sector=stock.sector
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock


# -------------------------
# ADD PRICE
# -------------------------
@router.post("/prices")
def add_price(price: PriceCreate, db: Session = Depends(get_db)):

    stock = db.query(Stock).filter(Stock.symbol == price.stock_symbol).first()

    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    new_price = HistoricalPrice(
        stock_id=stock.id,
        date=price.date,
        open_price=price.open_price,
        close_price=price.close_price,
        high_price=price.high_price,
        low_price=price.low_price,
        volume=price.volume
    )

    db.add(new_price)
    db.commit()
    db.refresh(new_price)

    return new_price


# -------------------------
# CALCULATE RETURNS
# -------------------------
@router.get("/stocks/{symbol}/returns")
def calculate_returns(symbol: str, db: Session = Depends(get_db)):

    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    prices = db.query(HistoricalPrice).filter(
        HistoricalPrice.stock_id == stock.id
    ).order_by(HistoricalPrice.date).all()

    if len(prices) < 2:
        return {"message": "Not enough data"}

    returns = []

    for i in range(1, len(prices)):
        prev_close = float(prices[i - 1].close_price)
        current_close = float(prices[i].close_price)

        daily_return = (current_close - prev_close) / prev_close

        returns.append({
            "date": prices[i].date,
            "daily_return": round(daily_return, 6)
        })

    return returns


# -------------------------
# CALCULATE VOLATILITY
# -------------------------
@router.get("/stocks/{symbol}/volatility")
def calculate_volatility(symbol: str, db: Session = Depends(get_db)):

    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    prices = db.query(HistoricalPrice).filter(
        HistoricalPrice.stock_id == stock.id
    ).order_by(HistoricalPrice.date).all()

    if len(prices) < 2:
        return {"message": "Not enough data"}

    returns = []

    for i in range(1, len(prices)):
        prev_close = float(prices[i - 1].close_price)
        current_close = float(prices[i].close_price)
        returns.append((current_close - prev_close) / prev_close)

    mean_return = sum(returns) / len(returns)

    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)

    volatility = math.sqrt(variance)

    return {
        "volatility": round(volatility, 6)
    }