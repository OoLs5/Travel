import scrapy
from xiecheng.items import HotelItem

offset = 0

class HotelSpider(scrapy.Spider):
    name = "hotel"
    allowed_domains = ["www.booking.cn"]
    # start_urls = ["https://www.booking.cn/searchresults.zh-cn.html?aid=39764&lang=zh-cn&sb=1&src_elem=sb&src=searchresults&dest_id=679&dest_type=region&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0"]

    def __init__(self, max_page=1, dest_id=678, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dext_id = dest_id
        self.url = 'https://www.booking.cn/searchresults.zh-cn.html?aid=39764&lang=zh-cn&sb=1&src_elem=sb&src=searchresults&dest_id={0}&dest_type=region&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0'.format(self.dext_id)
        self.max_page = (max_page-1)*25
        self.start_urls = [self.url]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en",
            "Cookie": "aliyungf_tc:72c6ee8fc9d7c7c809d80443af6e9d1faa7f06b05176f6811ecef488d5f60258;OptanonConsent=implicitConsentCountry=GDPR&implicitConsentDate=1701075538145&isGpcEnabled=0&datestamp=Mon+Nov+27+2023+18%3A00%3A12+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9e944c08-1d60-4217-a360-f3e6ee41c32e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false;_pxde=a5d4f23f21f2f56f219905e89908a855eaeaa021e2db9988face8df0d58b8f35:eyJ0aW1lc3RhbXAiOjE3MDExNTUxOTE3OTMsImZfa2IiOjAsImlwY19pZCI6W119;_px3=118ea42638944f970de9d4cefeffb56ec66b12bcb671d05e62005b0a8b4ff250:jc+psN/pb9Roi9bs5IKvu97vGVdSQGe9tPThVX0MsRJCLT1UVR/gCfZLe9nHTHpCG6pbhhcKnl0fpZpEIpKIBA==:1000:9mt1UlZg2GUTMmHVBKAMAIFIPlTDqpoaZCFT4xTp0PYDP9eHJr/UIA1cq9WgySe2NBQUlqvgwJfDb/+lxv+TfYsAAYh/tdOA/ztTwHyfUeGybkspoXI9zSTFuk7DK2BTaRnSZqn4uOSwjoLiX29qGseNZ0yMfq3mAij7DUGqcNLX/FeKbl5oG/WoThya/KfMylG8BbC9XerNnha1shsmI2frT0HKWi8dx5Wo/WRu4JU=;bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLblgO%2Fz4BDP5swgAVyklO36oP9ntvK13Oley%2BNgGAwQIOnbfwqGOKBF%2BlZNGF6tWacv9Z%2B8Tlajkl5ynQANFW3Lph6grb4THFXHqxVq%2Bj%2B4Hwk1Cbrvb%2FfI7le0N6alZBTilUw05JU4%2FSrWQJWwxeCNuJUZKc5eMnfZBzg7ly%2F118%3D;pxcts=cc6aec29-8db9-11ee-bb67-98e27187fa9f;_uetsid=ef83a5a08d0311eea5cda765f23ac278;_ga=GA1.2.1471473675.1701075539;_gcl_au=1.1.1829836972.1701075540;acw_tc=b659c29217011539613954535e9e06c80b779a46a2c376ea32b6a255d4;_gid=GA1.2.1508778429.1701075539;cors_js=1;_pxvid=33fa3aca-8d03-11ee-af0a-0cdc188283c1;_ga_A12345=GS1.1.1701153962.3.0.1701153962.0.0.0;bkng_sso_ses=e30;bkng_sso_session=e30;_uetvid=ef83a3908d0311ee85eeb7a8c2781b8e;_ga_FPD6YLJCJ7=GS1.1.1701153962.3.0.1701153962.60.0.0;cnfunco=1;"
        }  # 这里要额外加上一个cookie是为了绕过booking网站的检测（大概就是第一次程序作为客户端请求后网站会返回重定向一个检验cookie的网址，要在请求头加上所需cookie才能绕过302重定向，这个cookie
        # 的来源是通过浏览器真实访问后在Devtool工具里面找到的booking服务器第一次的respond，但这个cookie并不具有永久性，大概过几个星期或者几个月booking就会更换掉了。在这里要感谢国内师傅提供的hotel
        # 的索引文件和cookie寻找方法，虽然该前辈的hotel索引和cookie对现在已经不具备时效性，但提供的方法还是让我找到了成功绕过booking服务器的反爬的措施）

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        divs = response.xpath("//div[@class='c066246e13']")
        global offset
        offset += 25
        """
        测试输出
        print("*"*60)
        print(len(divs))
        print("*"*60)
        """

        for div in divs:
            picture = div.xpath("./div[1]/div[1]/a/img/@src").extract_first()
            hotel_name = div.xpath("./div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/h3/a/div[1]/text()").extract_first()
            location = div.xpath("./div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a/span/span[1]/text()").extract_first()
            points = div.xpath("./div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/a/span/div[1]/div[1]/text()").extract_first()
            visitors = div.xpath("./div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/a/span/div[1]/div[2]/div[2]/text()").extract_first()
            comment = div.xpath("./div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/text()").extract_first()

            item = HotelItem()
            item["picture"] = picture
            item["hotel_name"] = hotel_name
            item["location"] = location
            if not points:
                item["points"] = "0"  # 表示暂无评分
            else:
                item["points"] = points
            if not visitors:
                item["visitors"] = "暂无人评分"
            else:
                item["visitors"] = visitors
            if not comment:   # None的判断
                item["comment"] = "暂无介绍"
            else:
                item["comment"] = comment

            yield item

        if offset <= self.max_page:
            next_url = 'https://www.booking.cn/searchresults.zh-cn.html?aid=39764&lang=zh-cn&sb=1&src_elem=sb&src=searchresults&dest_id={0}&dest_type=region&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset={1}'.format(self.dext_id, offset)
            yield scrapy.Request(url=next_url, callback=self.parse, headers=self.headers)