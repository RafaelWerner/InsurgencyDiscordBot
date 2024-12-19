from app.service.say import Say

class SendMessage():
    async def run(self, message):
        await Say().run(message)
