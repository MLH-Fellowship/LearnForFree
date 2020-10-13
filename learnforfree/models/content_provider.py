import requests
from bs4 import BeautifulSoup
from search.elastic import SearchEngine

from . import course
import json

# edx search engine module
import search.elastic
import time
import objectpath

import re

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

        #page = 1
        #f = open("edx_courses.json", "w")
        #url1 = "https://courses.edx.org/api/courses/v1/courses?page_size=3000&page=1"
        #url2 = "https://courses.edx.org/api/courses/v1/courses?page_size=3000&page=2"
        #url3 = "https://courses.edx.org/api/courses/v1/courses?page_size=3000&page=3"

        #response = requests.get(url1)
        #json_data = "{\n\"page1\":" + response.text + ",\n\"page2\":"
        #response = requests.get(url2)
        #json_data = json_data + response.text + ",\n\"page3\":"
        #response = requests.get(url3)
        #json_data = json_data + response.text + "\n}"
        #f.write(json_data)

        #exit()

        with open("edx_courses.json") as f:
            line = f.read()
            file = json.loads(line)

        tree_obj = objectpath.Tree(file)
        print(tuple(tree_obj.execute('$..name')))

        print(crses)


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

