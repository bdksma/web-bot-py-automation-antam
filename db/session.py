from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Gunakan mysql (nama service docker) sebagai host
DATABASE_URL = "mysql+pymysql://antam_user2:antam_pass1234@mysql:3306/antam_bot"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,       # Cek koneksi sebelum digunakan
    pool_recycle=3600,        # Refresh koneksi setiap 1 jam
    pool_size=5,              # Jumlah koneksi standby
    max_overflow=10           # Tambahan koneksi jika sedang sibuk
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()