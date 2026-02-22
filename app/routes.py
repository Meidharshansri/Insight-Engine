from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Stock, HistoricalPrice
from app.schemas import StockCreate, PriceCreate

# Define router FIRST
router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- STOCK ENDPOINTS ----------------

@router.get("/stocks")
def get_stocks(db: Session = Depends(get_db)):
    return db.query(Stock).all()

@router.post("/stocks")
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    existing_stock = db.query(Stock).filter(Stock.symbol == stock.symbol).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail="Stock symbol already exists")

    new_stock = Stock(
        symbol=stock.symbol,
        company_name=stock.company_name,
        sector=stock.sector
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock

# ---------------- PRICE ENDPOINTS ----------------

@router.post("/prices")
def create_price(price: PriceCreate, db: Session = Depends(get_db)):

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


@router.get("/stocks/{symbol}/prices")
def get_prices(symbol: str, db: Session = Depends(get_db)):

    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    return db.query(HistoricalPrice).filter(
        HistoricalPrice.stock_id == stock.id
    ).all()