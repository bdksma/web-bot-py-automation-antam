from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from db.session import Base
import datetime

# =====================
# USERS
# =====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    phone = Column(String(20))
    antam_username = Column(String(100))
    antam_password = Column(String(255))

    preferred_min_gram = Column(Integer, default=5)
    preferred_max_gram = Column(Integer, default=50)

    status = Column(Enum("ACTIVE", "LOCKED"), default="ACTIVE")

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    queues = relationship("StoreQueue", back_populates="user")


# =====================
# STORES
# =====================
class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    store_code = Column(String(50))
    store_name = Column(String(100))
    city = Column(String(50))

    status = Column(Enum("ACTIVE", "INACTIVE"), default="ACTIVE")

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    queues = relationship("StoreQueue", back_populates="store")


# =====================
# TRANSACTIONS (Online Buy)
# =====================
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    gram = Column(Integer)
    va_number = Column(String(100))

    status = Column(Enum("PENDING", "SUCCESS", "FAILED"))

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="transactions")


# =====================
# STORE QUEUE (Antrean)
# =====================
class StoreQueue(Base):
    __tablename__ = "store_queue"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))

    queue_number = Column(String(50))

    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="queues")
    store = relationship("Store", back_populates="queues")
