import requests
from bs4 import BeautifulSoup
from search.elastic import SearchEngine

from . import course

# edx search engine module
import search.elastic

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
        elif self.name == 'who':
            data = self.scrape_data_who()
        else:
            raise NotImplementedError
        return data

    def scrape_data_edx(self):
        crses = []

        search_engine = SearchEngine.get_search_engine(index="courseware_index")
        print(search_engine)
        exit()
        
        crses = search_engine.search(query_string=self.keyword)
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

    def scrape_data_who(self):
        crses = []
        url = self.url + self.keyword
        dom = BeautifulSoup(requests.get(url).text, 'html.parser')
        html_courses = dom.find_all("div", attrs={"class": "course-group"})[0]
        html_courses = html_courses.find_all("div", attrs={"class": "course-item"})
        for html_course in html_courses:
            title = html_course.find_all("div", attrs={"class": "course-title"}).div.h4.a["title"]
            print(title)
            desc = html_course.find_all("div", attrs={"class": "course-description"}).div.div.p.contents
            href = html_course.find_all("div", attrs={"class": "course-title"}).div.h4.a["href"]
            link = 'https://www.openwho.org' + href
            img_link = html_course.find_all("a", attrs={"class": "course-image"}).a.picture.source["srcset"]
            img_link = img_link.split(",")[0]

            crs = course.Course(title, desc, self.name, link, img_link)
            crses.append(crs)
        return crses

