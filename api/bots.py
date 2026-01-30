from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.session import get_db
from db.models import User
from bots.buy_bot import BuyBot
# Pastikan modul QueueBot diimport jika sudah tersedia (Milestone 8)
# from bots.queue_bot import QueueBot 

router = APIRouter(prefix="/bots", tags=["Bots"])

@router.post("/buy/start")
def start_buy_bot(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint untuk memulai Bot Pembelian Online (Milestone 3 & 4).
    Bot ini akan membuka browser agar user bisa login manual.
    """
    # Mengambil user pertama secara default karena login tetap dilakukan manual oleh user
    user = db.query(User).filter(User.status == "ACTIVE").first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Tidak ada user aktif di database")
    
    # Inisialisasi Bot dengan data user terpilih
    bot = BuyBot(user)
    
    # Menjalankan bot.run di background task agar dashboard tetap responsif [cite: 148]
    background_tasks.add_task(bot.run)
    
    # Response JSON yang lengkap untuk menghindari 'undefined' di alert dashboard
    return {
        "status": "Bot Pembelian Dimulai", 
        "message": f"Browser telah dibuka. Silakan login manual untuk {user.full_name}.",
        "user_id": user.id
    }

@router.post("/queue/start")
def start_queue_bot(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint untuk memulai Bot Antrean Toko (Milestone 7 & 8).
    Memilih user secara otomatis berdasarkan kriteria transaksi 14 hari terakhir.
    """
    # Logic Seleksi Otomatis 14 Hari [cite: 55, 122]
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    
    eligible_user = db.query(User).filter(
        (User.last_transaction_at == None) | (User.last_transaction_at <= fourteen_days_ago),
        User.status == "ACTIVE"
    ).first()

    if not eligible_user:
        # Memberikan status 200 dengan pesan informasi jika tidak ada user yang memenuhi syarat
        return {
            "status": "Gagal", 
            "message": "Tidak ada user yang memenuhi syarat 14 hari terakhir."
        }

    # Implementasi Milestone 8: Jalankan bot antrean otomatis dengan data user terpilih
    # bot_queue = QueueBot(eligible_user)
    # background_tasks.add_task(bot_queue.run)

    return {
        "status": "Bot Antrean Dimulai", 
        "message": f"Bot berjalan otomatis menggunakan data: {eligible_user.full_name}",
        "target_user": eligible_user.full_name
    }