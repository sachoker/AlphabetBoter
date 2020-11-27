import collections
import string
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters


class DialogBot:

    def __init__(self, token, generator):
        self.updater = Updater(token=token)
        handler = MessageHandler(Filters.command | Filters.text, self.handle_message)
        self.updater.dispatcher.add_handler(handler)
        self.handlers = collections.defaultdict(generator)

    def start(self):
        self.updater.start_polling()

    def handle_message(self, update, context):
        print("Received", update.message)
        chat_id = update.message.chat_id
        if update.message.text == "/start":
            self.handlers.pop(chat_id, None)

        if chat_id in self.handlers:
            try:
                answer = self.handlers[chat_id].send(update.message)
            except StopIteration:
                del self.handlers[chat_id]

                return self.handle_message(update, context)
        else:
            answer = next(self.handlers[chat_id])

        print("Answer: %r" % answer)
        context.bot.sendMessage(chat_id=chat_id, text=answer)


def dialog():
    answer = yield "Hello! Write all your words and i will sort it."
    answer = answer.text.translate(str.maketrans('', '', string.punctuation))
    ls = answer.split()
    ls.sort()
    s = ""
    for i in ls:
        s = s + i + " "
    yield s


if __name__ == "__main__":
    token = "1416419333:AAHHU91rssCjG5X0bF9_-RLRC1mrqowKH1Q"
    bot = DialogBot(token, dialog)
    bot.start()
