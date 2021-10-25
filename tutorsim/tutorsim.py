from telegram.ext.conversationhandler import ConversationHandler
import contexts

from telegram import Update
from telegram.ext import  Updater, CommandHandler, CallbackContext

import pygsheets
from telegram.ext.dispatcher import Dispatcher

from config import TELEGRAM_API_KEY, GOOGLE_SERVICE_KEY, GOOGLE_SPREAD_SHEET, CourseInfo
from definitions import STATES



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


from course_mgr.course_info import CourseInfo
from course_mgr.course_handler import CourseHandler

logger = logging.getLogger(__name__)

gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)
sh = gc.open('2021 COME1101')

updater = Updater(TELEGRAM_API_KEY)
print(STATES)
c1 = CourseHandler(STATES, sh, CourseInfo("COME1101"))

sh = gc.open('2021 COME1103')
c2 = CourseHandler(STATES, sh, CourseInfo("COME1103"))

def start(update: Update, context: CallbackContext) -> int:
    text = "확인하고자 하는 과목을 입력해주세요."
    update.message.reply_text(text)
    return 0

def handle(update: Update, context: CallbackContext) -> int:
    text = "확인하고자 하는 과목을 입력해주세요."
    update.message.reply_text(text)
    return 1

def cancel(update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END

def come1103(update: Update, context: CallbackContext) -> int:
    return 0

def come1101(update: Update, context: CallbackContext) -> int:
    return 1

conv = ConversationHandler(
            entry_points=[CommandHandler('start', start), 
                          CommandHandler('COME1101', come1103),
                          CommandHandler('COME1103', come1101)],
            states={
                0: c1.get_conv_handler(),
                1: c2.get_conv_handler()
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )


updater.dispatcher.add_handler(conv)
updater.start_polling()
updater.idle()

