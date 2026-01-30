import sys
import asyncio
import time
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from fastapi import FastAPI
from api.users import router as users_router
from api.bots import router as bots_router
from api.dashboard import router as dashboard_router

from db.session import engine
from db.models import Base

# ⬇️ FUNGSI UNTUK MEMBUAT TABEL DENGAN RETRY LOGIC
def create_tables():
    retries = 5
    while retries > 0:
        try:
            print("Mencoba menghubungkan ke database...")
            Base.metadata.create_all(bind=engine)
            print("Database berhasil terhubung dan tabel telah dibuat!")
            break
        except OperationalError as e:
            retries -= 1
            print(f"Database belum siap. Mencoba lagi dalam 5 detik... (Sisa percobaan: {retries})")
            time.sleep(5)
    if retries == 0:
        print("Gagal terhubung ke database setelah beberapa kali percobaan.")

# ⬇️ LIFESPAN HANDLER (PENGGANTI @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kode di sini dijalankan saat startup
    create_tables()
    yield
    # Kode di sini dijalankan saat shutdown (jika diperlukan)

app = FastAPI(lifespan=lifespan)

app.include_router(dashboard_router)
app.include_router(users_router)
app.include_router(bots_router)

@app.get("/")
def root():
    return {"status": "ok"}