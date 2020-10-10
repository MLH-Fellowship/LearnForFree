import json


class Course:
    def __init__(self, course_name, course_desc, course_prov, course_link_url, course_img_url):
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_prov = course_prov
        self.course_link_url = course_link_url
        self.course_img_url = course_img_url

    def get_course_name(self):
        return self.course_name

    def get_course_desc(self):
        return self.course_desc

    def get_course_prov(self):
        return self.course_prov

    def get_course_link_url(self):
        return self.course_link_url

    def get_course_img_url(self):
        return self.course_img_url

    def set_course_name(self, course_name):
        self.course_name = course_name

    def set_course_desc(self, course_desc):
        self.course_desc = course_desc

    def set_course_prov(self, course_prov):
        self.course_prov = course_prov

    def set_course_link_url(self, course_link_url):
        self.course_link_url = course_link_url

    def set_course_img_url(self, course_img_url):
        self.course_img_url = course_img_url

    def as_dict(self):
        return dict(
            course_name=self.course_name,
            course_desc=self.course_desc,
            course_prov=self.course_prov,
            course_link_url=self.course_link_url,
            course_img_url=self.course_img_url
        )
