# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PricecomparatorPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #price
        key = 'price'
        value = adapter.get(key)
        if value == None:
            adapter[key] = int(0)
        else:
            value = value.replace('₹','')
            value = value.replace(',','')
            adapter[key] = int(value)
        
        #discount
        key = 'discount'
        value = adapter.get(key)
        if value == None:
            adapter[key] = int(0)
        else:
            value = value.replace('%','')
            value = value.replace(' off','')
            adapter[key] = int(value)

        # retailer
        key = 'retailer'
        value = adapter.get(key)
        value = value.capitalize()
        adapter[key] = value
        
        #ratings
        key = ['rating', 'seller_ratings']
        for k in key:
            value = adapter.get(k)
            if(value == None):
                adapter[k] = float(0)
            else:
                adapter[k] = float(value)
        
        return item



import mysql.connector

class SavingToDatabasePipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'garg7575@',
            database = 'products'
        )

        self.cur = self.conn.cursor()

        self.cur.execute('''
            create table if not exists flipkart (
                    id INT PRIMARY KEY auto_increment,
                    Retailer VARCHAR(30),
                    Title VARCHAR(256),
                    Price INT,
                    Discount INT,
                    Ratings FLOAT,
                    Seller VARCHAR(256),
                    Seller_ratings FLOAT,
                    Url VARCHAR(1000)
                );'''
        )

    def process_item(self, item, spider):
        self.cur.execute('''
            insert into flipkart (
                    Retailer, 
                    Title, 
                    Price, 
                    Discount, 
                    Ratings, 
                    Seller, 
                    Seller_ratings, 
                    Url
                ) values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,   
                    %s,
                    %s,
                    %s
                )
            ''' , (
                    item['retailer'],
                    item['title'],
                    item['price'],
                    item['discount'],
                    item['rating'],
                    item['seller'],
                    item['seller_ratings'],
                    item['url']    
                ))
        
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()