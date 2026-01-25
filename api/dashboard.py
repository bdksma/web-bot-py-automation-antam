from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import User, Store

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    stores = db.query(Store).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "stores": stores
        }
    )
