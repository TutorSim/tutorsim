from telegram import Update
from telegram.ext import  CommandHandler, ConversationHandler, CallbackContext

import pygsheets

from telegram_mgr.init_handler import InitHandler
from telegram_mgr.register_handler import RegisterHandler
from telegram_mgr.info_handler import InfoHandler
from telegram_mgr.score_handler import ScoreHandler

from telegram_mgr.course_info import CourseInfo

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class CourseHandler():
    def __init__(self, telegram_states:list, sheet:pygsheets.Spreadsheet, course:CourseInfo) -> None:
        self.sh = sheet
        self.course = course

        # Internal usages
        self.state_map = {state:idx for idx, state in enumerate(telegram_states)}
        self.handlers = [
                         InitHandler(self.state_map, self.sh),
                         RegisterHandler(self.state_map, self.sh),
                         InfoHandler(course),]

        for content in course.get_course_contents():
            self.handlers.append(ScoreHandler(self.state_map, self.sh, content))

        #self.handlers.append(CommandHandler('help', self.help))

    def get_conv_handler(self):
        conv_handlers = [x.get_handler() for x in self.handlers]
        conv_handlers.append(CommandHandler('help', self.help))

        conv = ConversationHandler(
            entry_points=[CommandHandler(f"{self.course.course_id}", self.greeting)],
            states={self.state_map["CONV_START"]: conv_handlers},
            fallbacks=[CommandHandler('cancel', self.cancel)],
            map_to_parent={
                ConversationHandler.END:ConversationHandler.END
            }
        )
        return [conv]

    def greeting(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(f"{self.course.course_id}")
        return self.state_map["CONV_START"]
    
    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END

    def help(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        #context.user_data.clear()

        resp = ""
        for handler in self.handlers:
            resp += handler.get_help()
            resp += "\n"

        update.message.reply_text(resp)    
        

