# bots/registry.py
class BotRegistry:
    _bots = {}

    @classmethod
    def add(cls, user_id, bot):
        cls._bots[user_id] = bot

    @classmethod
    def get(cls, user_id):
        return cls._bots.get(user_id)

    @classmethod
    def stop(cls, user_id):
        bot = cls._bots.get(user_id)
        if bot:
            bot.stop_browser()
            del cls._bots[user_id]
