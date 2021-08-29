from telegram.ext.conversationhandler import ConversationHandler
import contexts

from telegram import Update
from telegram.ext import  Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import pygsheets
from telegram.ext.dispatcher import Dispatcher

from config import TELEGRAM_API_KEY, GOOGLE_SERVICE_KEY, COURSE_LIST
from definitions import STATES



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


from course_mgr.course_handler import CourseHandler

logger = logging.getLogger(__name__)

class TelegramManager():
    def __init__(self, dp:Dispatcher, gsk:str, courseList:list):
        gc = pygsheets.authorize(service_file=gsk)

        self.courseList = courseList
        for course in courseList:
            sh = gc.open(course.get_sheet_name())
            handler = CourseHandler(STATES, sh, course)
            dp.add_handler(handler.get_conv_handler())
            
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('help', self.help))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_wrong_commands))
        
    def start(self, update: Update, context: CallbackContext) -> None:
        text = "확인하고자 하는 과목을 입력해주세요.\n"
        for course in self.courseList:
            text += f"/{course.course_id}: {course.course_name}\n"
        update.message.reply_text(text)
    
    def help(self, update: Update, context: CallbackContext) -> None:
        text = "시작하시려면 명령어 /start 로 시작하세요."
        update.message.reply_text(text)

    def handle_wrong_commands(self, update: Update, context: CallbackContext) -> None:
        text = "시작하시려면 명령어 /start 로 시작하세요."
        update.message.reply_text(text)

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END

updater = Updater(TELEGRAM_API_KEY)
tm = TelegramManager(updater.dispatcher, GOOGLE_SERVICE_KEY, COURSE_LIST)


updater.start_polling()
updater.idle()

