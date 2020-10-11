import requests
from bs4 import BeautifulSoup
from . import course


class ContentProvider:
    def __init__(self, provider_data):
        self.provider_name = provider_data["name"]
        self.provider_web_search_url = provider_data["web_search_url"]

    def provide(self, keyword):
        scrape = Scrape(self.provider_name, self.provider_web_search_url, keyword)
        return scrape.scrape_data()


class Scrape:
    def __init__(self, name, url, keyword):
        self.name = name
        self.url = url
        self.keyword = keyword

    def scrape_data(self):
        if self.name == 'edx':
            data = self.scrape_data_edx()
        elif self.name == 'futurelearn':
            data = self.scrape_data_fl()
        else:
            raise NotImplementedError
        return data

    def scrape_data_edx(self):
        crses = []
        url = self.url + self.keyword + '&tab=course'
        dom = BeautifulSoup(requests.get(url).text, 'html.parser')
        html_courses = dom.find_all("div", attrs={"class": "discovery-card"})
        html_courses.pop(0)
        html_courses.pop(0)
        html_courses.pop(0)
        html_courses.pop(0)
        for html_course in html_courses:
            title = html_course["aria-label"]
            print(title)
            desc = ''
            href = html_course.a["href"]
            link = 'https://www.edx.org' + href
            # img_link = html_course.div.div.div.img["href"]
            img_link = 'https://s3.amazonaws.com/media.al-fanarmedia.org/wp-content/uploads/2020/04/06213216/edx.jpg'

            crs = course.Course(title, desc, self.name, link, img_link)
            crses.append(crs)
        return crses

    def scrape_data_fl(self):
        crses = []
        url = self.url + self.keyword
        dom = BeautifulSoup(requests.get(url).text, 'html.parser')
        html_courses = dom.find_all("li", attrs={"class": "m-link-list__item"})
        for html_course in html_courses:
            title = html_course.div.h3.a.contents
            print(title)
            desc = html_course.div.p.contents
            href = html_course.div.h3.a["href"]
            link = 'https://www.futurelearn.com' + href
            img_link = ''

            crs = course.Course(title, desc, self.name, link, img_link)
            crses.append(crs)
        return crses

