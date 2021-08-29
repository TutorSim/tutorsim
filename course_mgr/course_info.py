class CourseInfo:
    PROFESSOR_NAME = 'PROFESSOR_NAME'
    CONTACT_EMAIL = 'PROFESSOR_EMAIL'
    CONTACT_OFFICE = 'PROFESSOR_PHONE'
    SCORE_CONTENTS = ['attendance', 'homework', 'quiz', 'midterm', 'final', 'total']

    def __init__(self, _id:str, c_name:str, p_name:str, email:str, contact:str, sheet_name:str, contents:list):
        self.course_id = _id
        self.course_name = c_name
        self.prof_name = p_name
        self.prof_email = email
        self.prof_phone = contact
        self.sheet_name = sheet_name
        self.contents = contents
        
    def get_text(self) -> str:
        return f"{self.course_id} {self.course_name} \n 담당교수:{self.prof_name}\n메일주소:{self.prof_email}\n전화번호:{self.prof_phone}\n"

    def get_course_contents(self) -> list:
        return self.contents

    def get_sheet_name(self) -> str:
        return self.sheet_name
    
    def get_functor(self, idx):
        def functor(update, context) -> int:
            return idx
        return functor