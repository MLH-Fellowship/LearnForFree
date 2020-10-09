import json


class Course:
    def __init__(self, coursename, coursedesc):
        self.coursename = coursename
        self.coursedesc = coursedesc

    def get_course_name(self):
        return self.coursename

    def get_course_desc(self):
        return self.coursedesc

    def set_course_name(self, coursename):
        self.coursename = coursename

    def set_course_desc(self, coursedesc):
        self.coursedesc = coursedesc

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)