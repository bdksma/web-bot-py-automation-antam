# bots/buy_bot.py
import time
from bots.base import BaseBot

ANTAM_URL = "https://www.logammulia.com"

class BuyBot(BaseBot):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def start(self):
        print(f"[BUY BOT] Starting for user {self.user.id}")

        self.start_browser(headless=False)
        self.page.goto(ANTAM_URL, timeout=60_000)

        self.wait_for_manual_login()
        self.monitor_and_buy()

    def wait_for_manual_login(self):
        print("[BUY BOT] Waiting for user to login manually...")

        # tanda user sudah login (sesuaikan selector real)
        self.page.wait_for_selector(
            "text=Logout",
            timeout=0   # tunggu SELAMANYA
        )

        print("[BUY BOT] Login detected!")

    def monitor_and_buy(self):
        print("[BUY BOT] Monitoring gold availability...")

        while self.running:
            try:
                self.page.reload()
                time.sleep(3)

                # contoh selector emas tersedia
                if self.page.locator("text=Buy").count() > 0:
                    print("[BUY BOT] Gold available, proceeding checkout")
                    self.checkout()
                    break

            except Exception as e:
                print("[BUY BOT ERROR]", e)
                time.sleep(5)

    def checkout(self):
        print("[BUY BOT] Checkout process started")

        # contoh (sesuaikan selector real)
        self.page.click("text=Buy")
        self.page.wait_for_timeout(2000)

        self.page.click("text=Checkout")
        print("[BUY BOT] Checkout completed")
