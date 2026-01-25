# bots/base.py
from playwright.sync_api import sync_playwright

class BaseBot:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.running = False

    def start_browser(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)

        # penting: persistent session
        self.context = self.browser.new_context()
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
