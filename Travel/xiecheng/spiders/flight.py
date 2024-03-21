import scrapy
from xiecheng.items import FlightItem


class FlightSpider(scrapy.Spider):
    name = "flight"
    allowed_domains = ["www.ly.com"]
    # start_urls = [
    #   "https://www.ly.com/flights/itinerary/oneway/CAN-XIY?from=%E6%B9%96%E5%8C%97&to=%E5%8C%97%E4%BA%AC&date=2023-11-29&fromairport=&toairport="]
    #   https://www.ly.com/flights/itinerary/oneway/CAN-PEK?from=%E5%B9%BF%E5%B7%9E&to=%E5%8C%97%E4%BA%AC&date=2023-11-30&fromairport=&toairport=&childticket=0,0

    def __init__(self, From='广州', To='北京', date='2023-12-11', *args, **kwargs):
        super(FlightSpider, self).__init__(*args, **kwargs)
        self.From = From
        self.To = To
        self.date = date
        self.url = "https://www.ly.com/flights/itinerary/oneway/-?from={0}&to={1}&date={2}&fromairport=&toairport=&childticket=0,0".format(From, To, date)
        # 网页中的oneway后面/-中“-”号左右两边分别是起点到终点的符号缩写，如果填错就不会有返回，这里选择不填服务器就会去根据他后面的from和to的字符来自动填充“-”左右两边的缩写
        self.start_urls = [self.url]

    def parse(self, response):
        divs = response.xpath("//div[@class='flight-item']")
        for div in divs:
            """
            plane 和 flight_company 和 tp的定位要注意
            """
            flight_company = div.xpath("./div[1]//div[@class='sec-part']/p/text()").extract_first()
            plane = div.xpath("./div[1]//div[@class='sec-part']/span/text()").extract_first()
            start_time = div.xpath("./div[1]//div[@class='head-times-info']/div[1]/strong/text()").extract_first()
            end_time = div.xpath("./div[1]//div[@class='head-times-info']/div[3]/strong/text()").extract_first()
            From = div.xpath("./div[1]//div[@class='head-times-info']/div[1]/em/text()").extract_first()
            To = div.xpath("./div[1]//div[@class='head-times-info']/div[3]/em/text()").extract_first()
            total_time = div.xpath("./div[1]//div[@class='head-times-info']/div[2]/i/text()").extract_first()
            food = div.xpath("./div[1]//div[@class='red-labels']/span/text()").extract_first()
            tp = div.xpath("./div[1]//div[@class='head-prices']/i[@class='gray-style']/text()").extract_first()
            cost = div.xpath("./div[1]//div[@class='head-prices']/strong/em/text()").extract_first()

            item = FlightItem()
            item['flight_company'] = flight_company
            item['plane'] = plane
            item['start_time'] = start_time
            item['end_time'] = end_time
            item['From'] = From
            item['To'] = To
            item['total_time'] = total_time
            item['food'] = food.split()[0]  # 除掉换行符
            item['tp'] = tp
            item['cost'] = cost

            yield item
