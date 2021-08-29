class CourseInfo:
    PROFESSOR_NAME = 'PROFESSOR_NAME'
    CONTACT_EMAIL = 'PROFESSOR_EMAIL'
    CONTACT_OFFICE = 'PROFESSOR_PHONE'
    SCORE_CONTENTS = ['attendance', 'homework', 'quiz', 'midterm', 'final', 'total']

    def __init__(self, _id:str):
        self.course_id = _id
        pass