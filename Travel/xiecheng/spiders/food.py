import scrapy
from xiecheng.items import FoodItem
page_num = 1

class FoodSpider(scrapy.Spider):
    name = "food"
    allowed_domains = ["www.xiachufang.com"]
    # start_urls = ["https://www.xiachufang.com/search/?keyword=广州&cat=1001&page=1"]

    def __init__(self, keyword='', *args, **kwargs):
        super(FoodSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.url = "https://www.xiachufang.com/search/?keyword={0}&cat=1001&page=1".format(keyword)
        self.start_urls = [self.url]

    def parse(self, response):
        ul = response.xpath("//ul[@class='list']")
        lis = ul.xpath("./li")
        global page_num

        for li in lis:
            img = li.xpath("./div[1]/a/div[1]/img/@data-src").extract_first()
            name = li.xpath("./div[1]/div[1]/p[1]/a/text()").extract_first()
            point = li.xpath("./div[1]/div[1]/p[3]/span[@class='score bold green-font']/text()").extract_first()

            item = FoodItem()
            item["img"] = img
            item["name"] = name.split()[0]
            if point:
                item["points"] = point
            else:
                item["points"] = "0"  # 暂无评分
            yield item

        if page_num <= 10:  # 默认只爬取10页信息
            page_num += 1
            yield scrapy.Request("https://www.xiachufang.com/search/?keyword={0}&cat=1001&page={1}".format(self.keyword, page_num))


