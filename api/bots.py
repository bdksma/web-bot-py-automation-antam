# api/bots.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import User
from bots.buy_bot import BuyBot
from bots.registry import BotRegistry
import threading

router = APIRouter(prefix="/bots", tags=["Bots"])

@router.post("/buy/start/{user_id}")
def start_buy_bot(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if BotRegistry.get(user_id):
        raise HTTPException(400, "Bot already running")

    bot = BuyBot(user)

    thread = threading.Thread(target=bot.start, daemon=True)
    thread.start()

    BotRegistry.add(user_id, bot)

    return {"status": "Buy bot started (manual login required)"}


@router.post("/buy/stop/{user_id}")
def stop_buy_bot(user_id: int):
    BotRegistry.stop(user_id)
    return {"status": "Buy bot stopped"}
