import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem
import re


def salary_clean(salary):
    spisok = []
    for line in salary:
        if line == 'з/п не указана':
            return line
        x = re.findall('\xa0', line)
        if len(x) > 0:
            line = line.replace('\xa0', "")
            spisok = spisok+[line]

    if len(spisok) > 1:
        return f'от {spisok[0]} до {spisok[1]}'
    else:
        return f'от {spisok}'


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://bizhbulyak.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a[data-qa="pager-next"]::attr(href)').get()
        
        yield response.follow(next_page, callback=self.parse)
        
        vacansy = response.css('a[data-qa="vacancy-serp__vacancy-title"]::attr(href)').getall()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.bloko-header-1::text').get()
        salary = response.css('span[data-qa="bloko-header-2"]::text').getall()
        salary = salary_clean(salary)
        # company = response.css('span[data-qa="bloko-header-2"]::text').getall()[-1]
        company = response.css('span[data-qa="bloko-header-2"]::text').getall()[-1]
        opisanie = response.css('div.g-user-content p::text').getall()
        key_skills = response.css('span[data-qa="bloko-tag__text"]::text').getall()
        # print(name, salary)
        
        yield JobparserItem(name=name, salary=salary, company=company, opisanie=opisanie, key_skills=key_skills)
