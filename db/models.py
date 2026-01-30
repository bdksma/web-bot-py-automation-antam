from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, TIMESTAMP, DateTime, Text
)
from sqlalchemy.orm import relationship
from db.session import Base
import datetime

# =====================
# USERS [cite: 48, 85, 148]
# =====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Kredensial Antam [cite: 35, 105]
    antam_username = Column(String(100), nullable=False, unique=True)
    antam_password = Column(String(255), nullable=False)
    
    # Integrasi Telegram [cite: 42, 60, 92]
    telegram_id = Column(String(50), nullable=True, unique=True)

    # Preferensi Pembelian [cite: 37, 72, 148]
    preferred_min_gram = Column(Integer, default=5)
    preferred_max_gram = Column(Integer, default=50)

    # Aturan Bisnis: Seleksi otomatis (14 Hari) [cite: 55, 122, 148]
    last_transaction_at = Column(DateTime, nullable=True)

    status = Column(
        Enum("ACTIVE", "LOCKED", name="user_status"),
        default="ACTIVE"
    )

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Relasi [cite: 50, 87]
    transactions = relationship("Transaction", back_populates="user")
    queues = relationship("StoreQueue", back_populates="user")


# =====================
# STORES [cite: 49, 86, 148]
# =====================
class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_code = Column(String(50), unique=True, nullable=False)
    store_name = Column(String(100), nullable=False)
    city = Column(String(50))

    status = Column(
        Enum("ACTIVE", "INACTIVE", name="store_status"),
        default="ACTIVE"
    )

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    queues = relationship("StoreQueue", back_populates="store")


# =====================
# TRANSACTIONS (Bot Pembelian Online) [cite: 33, 43, 88]
# =====================
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    gram = Column(Integer)
    # Output: Virtual Account [cite: 21, 41, 113]
    va_number = Column(String(100), nullable=True)
    
    # Log Bot (Opsional untuk audit) 
    log_message = Column(Text, nullable=True)

    status = Column(
        Enum("PENDING", "SUCCESS", "FAILED", name="transaction_status"),
        default="PENDING"
    )

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="transactions")


# =====================
# STORE QUEUE (Bot Antrean Toko) [cite: 46, 51, 89, 148]
# =====================
class StoreQueue(Base):
    __tablename__ = "store_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))

    # Output: Nomor Antrean [cite: 31, 58, 133]
    queue_number = Column(String(50), nullable=True)

    status = Column(
        Enum("PROCESSING", "COMPLETED", "FAILED", name="queue_status"),
        default="PROCESSING"
    )

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="queues")
    store = relationship("Store", back_populates="queues")