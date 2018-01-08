import scrapy
import re
import codecs
import json

class QuotesSpider(scrapy.Spider):
    name = "urlspider"
    days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    years = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]
    d = 0
    m = 0
    y = 0
    def start_requests(self):
        urls = [
            'http://www.thehindu.com/archive/print/2006/01/01/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
#        urls = response.xpath('//table[@class="cnt"][last()]//tr[last()]/td[@width="670"]/div[last()]//a/@href').extract()
        print(response.url)
        urlfilename = re.sub(r"\/|:", r"_", response.url)
        with open("./urlhtmls/%s" %urlfilename, 'wb') as g:
            g.write(response.body)
        urls = response.xpath('//ul[@class="archive-list"]//a/@href').extract()
        filename = 'urls.jl'
        with codecs.open(filename, 'a', 'utf-8') as f:
            for rl in urls:
                line = json.dumps(rl,ensure_ascii=False) + "\n"
                f.write(line)
        if(self.months[self.m] == "01" or self.months[self.m] == "03" or self.months[self.m] == "05" or self.months[self.m] == "07" or self.months[self.m] == "08" or self.months[self.m] == "10"):
            if(self.days[self.d] == "31"):
                self.m = self.m + 1
                self.d = 0
            else:
                self.d = self.d + 1
        elif(self.months[self.m] == "12"):
            if(self.days[self.d] == "31"):
                self.y = self.y + 1
                self.m = 0
                self.d = 0
            else:
                self.d = self.d + 1
        elif(self.months[self.m] == "04" or self.months[self.m] == "06" or self.months[self.m] == "09" or self.months[self.m] == "11"):
            if(self.days[self.d] == "30"):
                self.m = self.m + 1
                self.d = 0
            else:
                self.d = self.d + 1
        else:
            intyear = int(self.years[self.y])
            if(intyear % 4 == 0):
                if(self.days[self.d] == "29"):
                    self.m = self.m + 1
                    self.d = 0
                else:
                    self.d = self.d + 1
            else:
                if(self.days[self.d] == "28"):
                    self.m = self.m + 1
                    self.d = 0
                else:
                    self.d = self.d + 1
        if(self.years[self.y] == "2018" and self.months[self.m] == "01" and self.days[self.d] == "08"):
            print("Finished")
        else:
            url = "http://www.thehindu.com/archive/print/" + self.years[self.y] + "/" + self.months[self.m] + "/" + self.days[self.d] + "/"
            yield scrapy.Request(url, callback=self.parse)
#stopped at 37449 !!!
