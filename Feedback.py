class Feedback:
    count_id = 0

    def __init__(self, first_name, last_name,email,reason, report, rating, feedback):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__reason = reason
        self.__report = report
        self.__rating = rating
        self.__feedback = feedback

    def get_Feedback_id(self):
        return self.__feedback_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_reason(self):
        return self.__reason

    def get_report(self):
        return self.__report

    def get_rating(self):
        return self.__rating

    def get_feedback(self):
        return self.__feedback

    def set_Feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_reason(self,reason):
        self.__reason = reason

    def set_report(self,report):
        self.__report = report

    def set_rating(self, rating):
        self.__rating = rating

    def set_feedback(self, feedback):
        self.__feedback = feedback