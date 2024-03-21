import scrapy
from xiecheng.items import City_Name

count = 1  # 为收集携程网站的搜索列表所对应的城市的序号而定义的计算器

class CityNameSpider(scrapy.Spider):
    name = "city_name"
    handle_httpstatus_list = [404, 500]  # 在跑数据时发现携程网有反爬措施，即在html#sightname的城市文本中无规律的序号会返回404，所以此处进行404处理
    allowed_domains = ["you.ctrip.com"]
    start_urls = ["https://you.ctrip.com/sight/1/s0-p2.html#sightname"]

    def __init__(self, max_page=353, *args, **kwargs):
        super(CityNameSpider, self).__init__(*args, **kwargs)
        self.max = max_page

    def parse(self, response):
        global count

        div = response.xpath("//div[@class='f_left']")
        city_in_ch = div.xpath("./h1/a/text()").extract_first()
        city_in_en = div.xpath("./p/text()").extract_first()

        item = City_Name()
        item["City_In_Chinese"] = city_in_ch
        item["City_In_English"] = city_in_en
        item["num"] = count

        count += 1
        yield item

        if count < self.max:
            if count == 353:  # 注意当count=353时会跳转到一个不是期望爬取的网页，不会有item的返回，所以程序会在此中断，因而要注意避开353这个count
                count += 1
            next_url = "https://you.ctrip.com/sight/{0}/s0-p2.html#sightname".format(count)
            yield scrapy.Request(next_url)
