# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
import csv
import os

class CityNamePipeline:
    def open_spider(self, spider):
        if spider.name == "city_name":
            self.file = open("City.json", "ab")

    def process_item(self, item, spider):
        if spider.name == "city_name":  # 由于反爬会有一些序号没有城市数据而返回None,所以此处把None的不写入文档
            if str(item["City_In_Chinese"]) != "None":
                value = str(item["City_In_Chinese"]) + ' ' + str(item["City_In_English"]) + ':' + str(item["num"])
                content = json.dumps(value, ensure_ascii=False) + ';\n'
                self.file.write(content.encode('utf=8'))
        return item  # 这个return很重要，不然后面的Pipeline就接受不到item啦

    def close_spider(self, spider):
        if spider.name == "city_name":
            self.file.close()


class XiechengPipeline:
    def open_spider(self, spider):
        if spider.name == "XC":
            self.file = open("./景点/scene.csv", "w", encoding='utf-8-sig', newline='')
            self.tap = ['title', 'location', 'points', 'comments', 'img_link', 'visitor', 'say']
            self.writer = csv.DictWriter(self.file, fieldnames=self.tap)
            self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "XC":
            self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        if spider.name == "XC":
            self.file.close()

class FlightPipeline:
    def open_spider(self, spider):
        if spider.name == "flight":
            self.file = open("./航班/{0}_{1}--》{2}.csv".format(spider.date, spider.From, spider.To), "w", encoding='utf-8-sig', newline='')
            self.tap = ['flight_company', 'plane', 'start_time', 'end_time', 'total_time', 'From', 'To', 'food', 'cost', 'tp']
            self.writer = csv.DictWriter(self.file, fieldnames=self.tap)
            self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "flight":
            self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        if spider.name == "flight":
            self.file.close()

class HotelPipeline:
    def open_spider(self, spider):
        if spider.name == "hotel":
            self.file = open("./酒店/Hotel.csv", "w", encoding='utf-8-sig', newline='')
            self.tap = ['hotel_name', 'location', 'points', 'visitors', 'picture', 'comment']
            self.writer = csv.DictWriter(self.file, fieldnames=self.tap)
            self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "hotel":
            self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        if spider.name == "hotel":
            self.file.close()


class FoodPipeline:
    def open_spider(self, spider):
        if spider.name == "food":
            self.f = open("./美食/food.csv", "w", encoding='utf-8-sig', newline='')
            self.tap = ["name", "img", "points"]
            self.writer = csv.DictWriter(self.f, fieldnames=self.tap)
            self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "food":
            self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        if spider.name == "food":
            self.f.close()



