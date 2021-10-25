from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from pygsheets import Spreadsheet

from course_mgr.course_info import CourseInfo

class RegisterHandler():
    def __init__(self, course:CourseInfo, state_map:dict, sh:Spreadsheet):
        self.state_map = state_map
        self.sh = sh
        self.course = course

        self.handler = ConversationHandler(
            entry_points=[CommandHandler('register', self.handle_register_start)],
            states={
                self.state_map["GET_STUDENT_ID"]: [
                    MessageHandler(
                        Filters.regex(r'\d{5}'), self.handle_check_user
                    ),
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex(r'\d{5}')), self.handle_unwanted_data),
                ],
                self.state_map["ID_CHECKED"]: [
                    MessageHandler(
                        Filters.text & ~(Filters.command), self.handle_check_password
                    )
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
            map_to_parent={
                self.state_map["CONV_END"]:self.state_map["CONV_START"],
                ConversationHandler.END:ConversationHandler.END
            }
        )

    def get_handler(self) -> Dispatcher:
        return self.handler
    
    def get_help(self):
        return f"/register: Tutor봇으로 사용자 등록을 합니다. 다른 사람은 개인 점수를 확인하지 않도록 변경한 암호를 확인합니다."

    def unknown(self, update: Update, context: CallbackContext) -> int:
        context.user_data.clear()
        update.message.reply_text("처리하지 못하였습니다.\n학번부터 다시 입력해주세요.")
        return self.state_map["GET_STUDENT_ID"]

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        update.message.reply_text("취소 되었습니다.")
        update.message.reply_text("새로 시작하시려면 /start 명령어를 사용하세요.")
        return ConversationHandler.END

    def handle_unwanted_data(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("다시 입력해주세요.")
        return self.state_map[context.user_data['next_state']]
    
    def handle_register_start(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("학번을 입력해주세요.")
        context.user_data['next_state'] = "GET_STUDENT_ID"
        return self.state_map[context.user_data['next_state']]

    def check_valid_user(self, user_id:int) -> bool:
        wks = self.sh.worksheet('title','password')
        df = wks.get_as_df()

        user_data = df.index[df['id'] == user_id].tolist()
        if user_data:
            return user_data[0]
        else:
            return -1

    def handle_check_user(self, update: Update, context: CallbackContext) -> int:
        user_id = int(update.message.text)
        if (row := self.check_valid_user(user_id)) >= 0:
            context.user_data['id'] = user_id        
            context.user_data['row'] = row + 2
            context.user_data['next_state'] = "ID_CHECKED"

            update.message.reply_text("비밀번호를 입력해주세요.")
            return self.state_map[context.user_data['next_state']]
        else:
            update.message.reply_text("수강신청 등록이 안된 사용자입니다.\n담당교수님께 확인하시길 바랍니다.")
            update.message.reply_text(self.course.get_text())
            context.user_data.clear()
            return self.state_map["CONV_END"]

    def check_pasword(self, idx:int, pwd:str) -> bool:
        wks = self.sh.worksheet('title','password')
        if wks.get_value('D'+str(idx)) == pwd:
            return True
        else:
            return False

    def handle_check_password(self, update: Update, context: CallbackContext) -> int:
        if self.check_pasword(context.user_data['row'], update.message.text):
            wks = self.sh.worksheet('title','password')
            wks.update_value('E'+str(context.user_data['row']), update.effective_user.id)
            wks = self.sh.worksheet('title','access_records')
            wks.update_value('B'+str(context.user_data['row']), update.effective_user.id)

            update.message.reply_text("챗봇 서비스에 등록되었습니다.")
        else:
            update.message.reply_text("비밀번호가 맞지 않습니다. \n다시 시작하길 바랍니다.")
        
        update.message.reply_text(self.course.get_text())
        context.user_data.clear()
        return self.state_map["CONV_END"]
