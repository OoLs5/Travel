import scrapy
from xiecheng.items import XiechengItem

count = 2  # 访问网址的网页

class XcSpider(scrapy.Spider):
    name = "XC"
    allowed_domains = ["you.ctrip.com"]
    # start_urls = ["https://you.ctrip.com/sight/1/s0-p2.html#sightname"]

    def __init__(self, num='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = num
        self.url = "https://you.ctrip.com/sight/{0}/s0-p2.html#sightname".format(num)
        self.start_urls = [self.url]

    def parse(self, response):
        divs = response.xpath("//div[@class='list_mod2']")
        global count
        count += 1
        """
        print("*" * 50)
        print(len(divs))
        print("*" * 50)  # 查看网页是否有结果输出
        """
        for div in divs:
            img = div.xpath("./div[1]/a/img/@src").extract()[0]
            title = div.xpath("./div[2]/dl/dt/a/text()").extract()[0]
            location = div.xpath("./div[2]/dl/dd[1]/text()").extract()[0]
            points = div.xpath("./div[2]/ul/li[1]/a/strong/text()").extract()
            comments = div.xpath("./div[2]/ul/li[3]/a/text()").extract()[0]
            visitor = div.xpath("./p/span/a/text()").extract()
            say = div.xpath("./p").extract()

            item = XiechengItem()
            item['img_link'] = img
            item['title'] = title
            item['location'] = location.split()[0]
            item['comments'] = comments.split()[0]
            if len(say):            # 以下三个if是对没有信息获取的判断
                item['say'] = say[0].split('/span>')[1].split('\r\n')[0]  # 进行信息处理，所需的评论信息包含在</span>和‘\r\n’之间，所以用两个split()来分割
            else:
                item['say'] = '暂无用户评价'
            if len(visitor):
                item['visitor'] = visitor[0]
            else:
                item['visitor'] = '暂无游客评论'
            if len(points):
                item['points'] = points[0]
            else:
                item['points'] = '0'  # 表示暂无评分

            yield item

        if count <= 10:  # 爬取10页数据（后期可自行调整，这里为了方便测试）
            next_url = "https://you.ctrip.com/sight/{0}/s0-p{1}.html#sightname".format(self.num, count)
            yield scrapy.Request(next_url)





