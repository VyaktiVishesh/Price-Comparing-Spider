import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import asyncioreactor
from scrapy.utils.project import get_project_settings
import sys
import os
from pick import pick
import mysql.connector
import urllib
import json


#Myntra Spider
class MyntraspiderSpider(scrapy.Spider):
    name = "myntraSpider"
    allowed_domains = ["myntra.com"]

    # overWrites specific settings of settings
    custom_settings = {
        # 'FEEDS' : {
        #     'booksdata.json' : {'format' : 'json', 'overwrite' : True},
        # }
    }

    def start_requests(self):
        yield scrapy.Request(f'https://myntra.com/search?q={Product_name}')

    def parse(self, response):
        items = response.css('div[data-id]')

        for item in items:
            relative_url = item.css('a[rel] ::attr(href)').get()
            item_url = f'https://flipkart.com{relative_url}'

            yield response.follow(relative_url, callback=self.parse_item)


    def parse_item(self, response):
        page = response
        yield{
            'retailer' : 'myntra',
            'title' : page.css('h1 ::text').get(),
            'price' : page.css('div ._30jeq3 ::text').get(),
            'discount' : page.css('div ._3Ay6Sb ::text').get(),
            'rating' : page.css('div ._3LWZlK ::text').get(),
            # 'number_ratings' : k,
            # P['number_reviews'] = y
            'seller' : page.css('div #sellerName ::text').get(),
            'seller_ratings' : page.css('div #sellerName div ::text').get(),
            'url' : page.url
        }


class FlipkartspiderSpider(scrapy.Spider):
    name = "flipkartSpider"
    allowed_domains = ["flipkart.com"]

    # overWrites specific settings of settings
    custom_settings = {
        # 'FEEDS' : {
        #     'booksdata.json' : {'format' : 'json', 'overwrite' : True},
        # }
    }

    def start_requests(self):
        yield scrapy.Request(f'https://flipkart.com/search?q={Product_name}')

    def parse(self, response):
        items = response.css('div[data-id]')

        for item in items:
            relative_url = item.css('a[rel] ::attr(href)').get()
            item_url = f'https://flipkart.com{relative_url}'

            yield response.follow(relative_url, callback=self.parse_item)


    def parse_item(self, response):
        page = response
        yield{
            'retailer' : 'flipkart',
            'title' : page.css('h1 ::text').get(),
            'price' : page.css('div ._30jeq3 ::text').get(),
            'discount' : page.css('div ._3Ay6Sb ::text').get(),
            'rating' : page.css('div ._3LWZlK ::text').get(),
            # 'number_ratings' : k,
            # P['number_reviews'] = y
            'seller' : page.css('div #sellerName ::text').get(),
            'seller_ratings' : page.css('div #sellerName div ::text').get(),
            'url' : page.url
        }



# Starts the Crawler for specific Product
def startCrawling():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(FlipkartspiderSpider)
    process.start() 


def start():
    startCrawling()
    startup_question = f"How you want to index {Product_name} items ? "
    options = ['Price', 'Ratings', 'Discount', 'Seller_Ratings']

    selected_option, index = pick(options, startup_question, indicator="->")

    #connecting to database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="garg7575@",
    database="products"
    )

    mycursor = mydb.cursor()

    if index == 0:
        mycursor.execute(f"Select Price, Title, Discount, Ratings, Seller, Seller_ratings, Url From flipkart order by Price limit {entries};")
        result = mycursor.fetchall()
    elif index == 1:
        mycursor.execute(f"Select Price, Title, Discount, Ratings, Seller, Seller_ratings, Url From flipkart order by Ratings desc limit {entries};")
        result = mycursor.fetchall()
    elif index == 2:
        mycursor.execute(f"Select Price, Title, Discount, Ratings, Seller, Seller_ratings, Url From flipkart order by Discount desc limit {entries};")
        result = mycursor.fetchall()
    else:
        mycursor.execute(f"Select Price, Title, Discount, Ratings, Seller, Seller_ratings, Url From flipkart order by Seller_ratings desc limit {entries};")
        result = mycursor.fetchall()

    mycursor.execute("Drop table flipkart;")
    mydb.commit()

    mycursor.close()
    mydb.close()

    #creating json file for output
    ind = 0
    obj = dict()
    for x in result:
        obj [ind] = {
            'Price' : x[0],
            'Title' : x[1],
            'Discount' : x[2],
            'Ratings' : x[3],
            'Seller' : x[4],
            'Seller_Ratings' : x[5],
            'Url' : urllib.parse.quote_plus(x[6])
        }
        ind += 1
    
    print(obj)
    jString = json.dumps(obj)
    jsonFile = open(f"{Product_name}.json", "w")
    jsonFile.write(jString)
    jsonFile.close()


# functions chain reaction starts from here:
Product_name = input('What product you are searching for? ')


entries = input('How many entries you want? ')

entries = int(entries)
start();



