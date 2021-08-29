from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from telegram_mgr.course_info import CourseInfo

class InfoHandler():
    def __init__(self, info:CourseInfo):
        self.information = info
        self.handler = CommandHandler('info', self.info)
            
    def get_handler(self) -> Dispatcher:
        return self.handler

    def get_help(self):
        return f"/info: 수업 관련 정보를 확인할 수 있습니다."

    def cancel(self, update: Update, context: CallbackContext) -> None:
        """Display the gathered info and end the conversation."""
        update.message.reply_text("취소 되었습니다.")
        context.user_data.clear()

    def info(self, update: Update, context: CallbackContext) -> None:
        text = self.information.get_text()
        update.message.reply_text(text)