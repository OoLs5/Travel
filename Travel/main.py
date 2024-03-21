import sys, os
import pandas as pd
import matplotlib.pyplot as plt
import scrapy
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import scrapydo
from scrapy.utils.project import get_project_settings
from xiecheng.spiders.XC import XcSpider
from xiecheng.spiders.city_name import CityNameSpider
from xiecheng.spiders.flight import FlightSpider
from xiecheng.spiders.food import FoodSpider
from xiecheng.spiders.hotel import HotelSpider
import datetime

CityDic = {}  # 城市序号, 方便用户定向查找需要查询的城市的景点信息
HotelDic = {}  # 方便用户定向查找需要查询的各个省份的酒店的信息


def Make_CityDic():
    """
    处理City.json文件的信息并把结果储存在字典CityDic里
    """
    File = open("City.json", "r", encoding='utf8')
    line = File.readline()
    while line:
        ls = line.split()
        CityName = ls[0].split('"')[1]
        Num = ls[len(ls) - 1].split(":")[1].split('"')[0]  # 这个返回的是str类型，所以在下面加入字典后会转化为int类型的值
        CityDic[CityName] = int(Num)
        line = File.readline()
    File.close()


def Make_HotelDic():
    """
    处理hotel.txt文件的信息并把结果储存在字典HotelDic里
    """
    File = open("Hotel.txt", "r", encoding='utf8')
    line = File.readline()
    while line:
        ls = line.split(',')
        Province = ls[0]
        value = ls[1:]  # 这个用的时候要转换为int
        HotelDic[Province] = value
        line = File.readline()
    File.close()


def Draw_it(FileName='', realrank=True):
    """
    显示top30柱状图
    """
    df = pd.read_csv(FileName)
    df_sorted = df.sort_values(by='points', ascending=False)
    if realrank:
        top100 = df_sorted.head(40).tail(30)  # 有一些评分含有水分所以筛选去掉头10个
    else:
        top100 = df_sorted.head(30)
    scenes = top100.iloc[:, 0]  # 第一列是名称
    points = top100.iloc[:, 2]  # 第三列是评分
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.barh(scenes, points, color='skyblue')
    plt.xlabel('评分')
    plt.ylabel(FileName.split('/')[1].split('.')[0])
    plt.title('Top 30')
    plt.gca().invert_yaxis()
    plt.subplots_adjust(left=0.38, right=0.95, top=0.9, bottom=0.1)
    # plt.tight_layout()
    plt.show()


def FindToDraw(FileName):
    """
    在生成文件中寻找目标画图文件
    :param FileName:
    :return:
    """
    if os.path.exists("./景点/" + FileName + ".csv"):
        Draw_it("./景点/" + FileName + ".csv")
    elif os.path.exists("./酒店/" + FileName + ".csv"):
        Draw_it("./酒店/" + FileName + ".csv")
    elif os.path.exists("./美食/" + FileName + ".csv"):
        Draw_it("./美食/" + FileName + ".csv", realrank=False)
    else:
        return True


class InputError(Exception):
    """
    定义用户输入异常类
    """

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


def GetCity(city):
    """
    获取城市旅游信息
    :param city:
    :return:
    """
    if os.path.exists("./景点/" + city + "景点.csv"):
        print("已生成{0}景点".format(city + ".csv"))
    elif city not in CityDic:
        print("暂无{0}的信息".format(city))
    else:
        num = CityDic[city]
        scrapydo.run_spider(XcSpider, num=num, settings=settings)
        os.rename("./景点/scene.csv", "./景点/{0}景点.csv".format(city))
        print("新生成{0}景点".format(city + ".csv"))


def GetFligt(From, To, Date):
    """
    获取航班信息
    :param From:
    :param To:
    :param Date:
    :return:
    """
    if os.path.exists("./航班/" + "{0}_{1}--》{2}.csv".format(Date, From, To)):
        print("已存在该航班信息")
    else:
        scrapydo.run_spider(FlightSpider, From=From, To=To, date=Date, settings=settings)
        print("新生成" + "{0}_{1}->{2}.csv".format(Date, From, To))


def GetHotel(Province):
    """
    获取旅店信息
    :param Province:
    :return:
    """
    if Province not in HotelDic:
        print("没有{0}的酒店信息".format(Province))
    elif os.path.exists("./酒店/" + Province + "酒店.csv"):
        print("已生成{0}酒店.csv".format(Province))
    else:
        max_page = int(HotelDic[Province][0])
        ID = int(HotelDic[Province][1])
        scrapydo.run_spider(HotelSpider, max_page=max_page, dest_id=ID, settings=settings)
        os.rename("./酒店/Hotel.csv", "./酒店/{0}酒店.csv".format(Province))
        print("新生成{0}酒店.csv".format(Province))


def GetFood(keyword):
    """
    获取美食信息
    :param keyword:
    :return:
    """
    if os.path.exists("./美食/{0}美食.csv".format(keyword)):
        print("已生成{0}美食.csv".format(keyword))
    else:
        scrapydo.run_spider(FoodSpider, keyword=keyword, settings=settings)
        os.rename("./美食/food.csv", "./美食/{0}美食.csv".format(keyword))
        print("新生成{0}美食.csv".format(keyword))


def travel(To, From='广州', num=3):
    """
    一键生成旅游目的地的相关信息, 默认是未来三天的航班
    :param To:
    :param From: 出发地默认是广州
    :return:
    """
    GetFood(To)
    GetCity(To)
    GetHotel(To)
    for i in range(num):
        day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        GetFligt(From, To, "{0}-{1}-{2}".format(day.split("-", 2)[0], day.split("-", 2)[1], day.split("-", 2)[2]))


def UpdateCity(num):
    """
    更新City.json文件
    :param num:更新页数，默认已经更新到500，如果需要更新建议超过500
    :return:
    """
    # process.crawl(CityNameSpider, max_page=num)
    # process.start()
    scrapydo.run_spider(CityNameSpider, max_page=num, settings=settings)
    print("已更新City.json")


def ReviewFile(FILE=""):
    """
    读取文件信息
    :param FILE:
    :return:
    """
    f = open(FILE, "r", encoding="utf-8")
    line = f.readline()
    while line:
        print(line)
        line = f.readline()
    f.close()


def Loading():
    """
    正在更新
    :return:
    """
    print("-" * 50)
    print("正在更新文件 ...")
    print("-" * 50)


def Travel():
    """
    操作表单
    :return:
    """
    print("-" * 50)
    print("欢迎使用Travel,输入help可查看帮助")
    print("-" * 50)
    do = input("Travel> ")
    while do != "exit()":
        command = do.split(None, 1)[0]
        rest = do.split(None, 1)[1:]
        try:
            match command:
                case "help":  # -h
                    ReviewFile("README.txt")
                case "city":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    else:
                        Loading()
                        GetCity(rest[0])
                case "flight":
                    try:
                        ls = rest[0].split()
                    except IndexError:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    if len(ls) != 3:
                        raise InputError("ArgumentNumError:{0}参数个数错误".format(command))
                    else:
                        try:  # 判断输入时间格式
                            datetime.datetime.strptime(ls[2], '%Y-%m-%d')
                        except ValueError:
                            raise InputError("TimeStrError:时间格式应是Year-mon-day")
                        Loading()
                        GetFligt(ls[0], ls[1], ls[2])
                case "hotel":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    else:
                        Loading()
                        GetHotel(rest[0])
                case "food":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    else:
                        Loading()
                        GetFood(rest[0])
                case "travel":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    ls = rest[0].split()
                    if len(ls) > 3:
                        raise InputError("TooMuchArgument:{0}参数过多".format(command))
                    else:
                        Loading()
                        match len(ls):
                            case 1:
                                travel(ls[0])
                            case 2:
                                travel(ls[0], ls[1])
                            case 3:
                                try:
                                    num = int(ls[2])  # 把参数3转化为int类型数字
                                except ValueError:
                                    raise InputError("ArgumentTypeError:{0}参数:{1}类型错误".format(command, ls[2]))
                                travel(ls[0], ls[1], num)

                case "read":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    elif not os.path.exists(rest[0]):
                        raise InputError("FileNotFound:没有找到{0}".format(rest[0]))
                    else:
                        ReviewFile(rest[0])
                case "update":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    else:
                        try:
                            num = int(rest[0])
                        except ValueError:
                            raise InputError("ArgumentTypeError:{0}参数:{1}类型错误".format(command, rest[0]))
                        Loading()
                        UpdateCity(num)
                case "draw":
                    if not rest:
                        raise InputError("ArgumentLost:{0}缺少参数".format(command))
                    else:
                        NotFound = FindToDraw(rest[0])
                        if NotFound:
                            raise InputError("FileNotFound:没有找到{0}".format(rest[0]))
                case _:
                    raise InputError("CommandError:无法识别命令{0}".format(command))

        except InputError as e:
            print(e)

        do = input("Travel> ")


if __name__ == "__main__":
    Make_CityDic()
    Make_HotelDic()  # 更新字典
    settings = get_project_settings()
    configure_logging(settings)
    scrapydo.setup()
    Travel()
