from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from pygsheets import Spreadsheet

class ScoreHandler():
    def __init__(self,state_map:dict, sh:Spreadsheet, sh_name:str):
        self.state_map = state_map
        self.sh = sh
        self.sheet_name = sh_name
        self.handler = ConversationHandler(
            entry_points=[CommandHandler(sh_name, self.show_menu)],
            states={
                self.state_map["HANDLE_SUMMARY_DETAIL"]: [
                    CommandHandler("summary", self.summary),
                    CommandHandler("detail", self.detail)
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

    def get_handler(self) -> Dispatcher:
        return self.handler

    def get_help(self):
        return f"/{self.sheet_name}: {self.sheet_name} 점수를 확인합니다."

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END
    
    def check_registered_user(self, _id:int) -> int:
        wks = self.sh.worksheet('title','password')
        df = wks.get_as_df()

        user_data = df.index[df['telegram_id'] == _id].tolist()
        if user_data:
            return user_data[0]
        else:
            return -1

    def show_menu(self, update: Update, context: CallbackContext) -> int:
        if (row := self.check_registered_user(update.effective_user.id)) > 0:
            context.user_data['gs_user_row'] = row
            update.message.reply_text("점수만 확인하려면 /summary를 입력하세요.\n자세한 정보를 확인하려면 /detail을 입력하세요.")
            return self.state_map["HANDLE_SUMMARY_DETAIL"]
        else:
            update.message.reply_text("사용자 등록을 먼저 하시길 바랍니다.")
            return ConversationHandler.END

    def summary(self, update: Update, context: CallbackContext) -> int:
        wks = self.sh.worksheet('title', self.sheet_name)
        df = wks.get_as_df()
        score = df.loc[context.user_data['gs_user_row'],'Total']
        update.message.reply_text(f"당신의 {self.sheet_name}의 점수는 {score}입니다.")
        context.user_data.clear()
        return ConversationHandler.END

    def detail(self, update: Update, context: CallbackContext) -> int:
        wks = self.sh.worksheet('title', self.sheet_name)
        df = wks.get_as_df()
        
        res = df.loc[context.user_data['gs_user_row'], :]
        values = list(res)

        response = ""
        for idx, col in enumerate(df.columns):
            if idx == 0 or idx == 1:
                continue
            response += f"{col}: {values[idx]}\n"
            
        update.message.reply_text(f"당신의 구체적인 {self.sheet_name}의 점수는 다음과 같습니다.\n{response}")
        context.user_data.clear()
        return ConversationHandler.END