# bots/base.py
from typing import Optional

class BaseBot:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.running = False

    def start_browser(self, headless: bool = True):
        if self.running:
            return

        # import DI DALAM method (anti crash)
        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="id-ID",
        )

        self.page = self.context.new_page()
        self.running = True

    def stop_browser(self):
        self.running = False

        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()