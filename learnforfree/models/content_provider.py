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

        # DONT RUN THE CODE
        # this script below fetches data from the edx api and saves it locally in the root
        # we use this file to then search for courses.
        # the file is already fetched! it takes 1hr

        #page = 0
        #f = open("edx_courses.json", "w", encoding="utf-8")
        #while True:
        #    page += 1
        #    url = 'https://courses.edx.org/api/courses/v1/courses?page_size=3000&page=' + str(page)
        #    json_data = ''
        #    try:
        #        response = requests.get(url)
        #        if response.status_code == 404:
        #            raise BufferError
        #        if page == 1:
        #            json_data += '{\n'
        #        key = '\"page' + str(page) + '\":\n'
        #        json_data += key
        #        json_data += response.text
        #        json_data += ',\n'
        #        f.write(json_data)
        #    except:
        #        <last char which is a , needs to be removed!>
        #        json_data += '}'
        #        f.write(json_data)
        #        f.close()
        #        break
        #exit()

        with open("edx_courses.json", "r", encoding="utf-8") as f:
            file = json.load(f)



        tree_obj = objectpath.Tree(file)

        names = []

        for results in tree_obj.execute('$..results'):
            for result_key, result_content in results.items():
                img_url = ''
                if result_key == "media":
                    img_url = result_content.get("image").get("small")
                if result_key == "name":
                    if self.keyword.lower() in result_content.lower():
                        name = result_content
                        if name not in names:
                            names.append(name)
                        else:
                            continue # there are some duplicates
                        crses.append(course.Course(name, 'Course description', self.name, 'some_url', img_url))

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

