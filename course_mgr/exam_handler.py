from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

import pygsheets

class ExamHandler():
    def __init__(self, sheet:pygsheets.Spreadsheet ):
        self.sh = sheet
        self.handler = CommandHandler('exam', self.info)
            
    def get_handler(self) -> Dispatcher:
        return self.handler

    def get_help(self):
        return f"/exam: 지난 시험 문제를 확인할 수 있습니다."

    def cancel(self, update: Update, context: CallbackContext) -> None:
        """Display the gathered info and end the conversation."""
        update.message.reply_text("취소 되었습니다.")
        context.user_data.clear()

    def info(self, update: Update, context: CallbackContext) -> None:
        wks = self.sh.worksheet('title','past_exam')
        df = wks.get_as_df()

        contents = []
        for idx, row in df.iterrows():
            contents.append(str(row[0]) + ":" + str(row[1]))

        update.message.reply_text("\n".join(contents))
        update.message.reply_text("명령어 목록을 확인하시려면 /help 명령어를 입력하세요.")