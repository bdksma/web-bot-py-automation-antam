from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models import User, Store

# ⬇️ penting: kasih prefix biar rapi & konsisten
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ⬇️ path relatif dari WORKDIR (/app)
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    stores = db.query(Store).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "stores": stores,
        }
    )