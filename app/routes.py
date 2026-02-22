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
        prev_close = float(prices[i-1].close_price)
        current_close = float(prices[i].close_price)

        daily_return = (current_close - prev_close) / prev_close

        returns.append({
            "date": prices[i].date,
            "daily_return": round(daily_return, 4)
        })

    return returns

import math

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
        prev_close = float(prices[i-1].close_price)
        current_close = float(prices[i].close_price)
        returns.append((current_close - prev_close) / prev_close)

    mean_return = sum(returns) / len(returns)

    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)

    volatility = math.sqrt(variance)

    return {
        "volatility": round(volatility, 6)
    }