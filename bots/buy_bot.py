# bots/buy_bot.py
import time
from bots.base import BaseBot

ANTAM_URL = "https://www.logammulia.com/id/purchase/gold"


class BuyBot(BaseBot):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.running = True

    def run(self):
        """
        Dipanggil oleh background_tasks.add_task(bot.run)
        """
        print(f"[BUY BOT] Memulai bot untuk user: {self.user.full_name}")

        try:
            # 1. Jalankan browser (manual login)
            self.start_browser(headless=False)

            # 2. Buka halaman Antam
            print(f"[BUY BOT] Membuka URL: {ANTAM_URL}")
            self.page.goto(ANTAM_URL, timeout=60000)

            # 3. Tunggu login manual
            self.wait_for_manual_login()

            # 4. Monitoring stok & auto-buy
            self.monitor_and_buy()

        except Exception as e:
            print(f"[BUY BOT CRITICAL ERROR]: {e}")

        finally:
            print("[BUY BOT] Selesai. Browser akan ditutup dalam 5 menit.")
            time.sleep(300)
            self.stop_browser()

    def wait_for_manual_login(self):
        print("[BUY BOT] Silakan LOGIN manual di browser...")
        try:
            # Deteksi tombol logout (tanda login sukses)
            self.page.wait_for_selector("text=Keluar", timeout=0)
            print("[BUY BOT] Login terdeteksi.")
        except Exception as e:
            print(f"[BUY BOT] Gagal mendeteksi login: {e}")

    def monitor_and_buy(self):
        print("[BUY BOT] Mulai monitoring stok emas...")

        while self.running:
            try:
                self.page.reload(wait_until="networkidle")
                time.sleep(3)

                print("[BUY BOT] Mengecek stok...")
                buy_button = self.page.locator(
                    "button:has-text('TAMBAH KE KERANJANG')"
                ).first

                if buy_button and buy_button.is_visible():
                    print("[BUY BOT] STOK TERSEDIA! Checkout dimulai.")
                    self.checkout()
                    break

                # Delay aman (anti rate-limit)
                time.sleep(10)

            except Exception as e:
                print(f"[BUY BOT] Error monitoring: {e}")
                time.sleep(5)

    def checkout(self):
        print("[BUY BOT] Proses checkout dimulai...")

        try:
            # Tambah ke keranjang
            self.page.click("button:has-text('TAMBAH KE KERANJANG')")
            self.page.wait_for_timeout(2000)

            # Buka cart
            self.page.goto("https://www.logammulia.com/id/cart", timeout=60000)
            self.page.wait_for_selector("text=CHECKOUT", timeout=15000)
            self.page.click("text=CHECKOUT")

            print("[BUY BOT] Jika captcha muncul, selesaikan manual.")
            print("[BUY BOT] Menunggu Virtual Account...")

            # Browser sengaja dibiarkan terbuka
            print("[BUY BOT] SUKSES! VA kemungkinan sudah muncul.")

        except Exception as e:
            print(f"[BUY BOT] Checkout gagal: {e}")

    def stop(self):
        """Dipanggil dari dashboard"""
        print("[BUY BOT] Stop signal diterima.")
        self.running = False
