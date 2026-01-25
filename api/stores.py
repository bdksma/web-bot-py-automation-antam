from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import Store

router = APIRouter(prefix="/stores")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()

@router.post("/")
def create_store(data: dict, db: Session = Depends(get_db)):
    store = Store(**data)
    db.add(store)
    db.commit()
    return {"status": "ok"}