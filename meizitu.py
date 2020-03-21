import urllib3
import re
import time
import random
import os


class Meizitu():

    # 初始化
    def __init__(self):
        self.url_all = 'https://www.mzitu.com/all/'
        self.url_old = 'https://www.mzitu.com/old/'
        self.http = urllib3.PoolManager()
        self.useragents = [
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)",
        ]
        self.picture_list = []  # 待下载图片地址列表
        self.headers = {
            'User-Agent': random.choice(self.useragents)
        }

    # 总程序
    def start(self, method='all', start_page=0):
        path = 'E:/meizitu/'
        if os.path.exists(path):
            print('文件夹：meizitu 已存在')
        else:
            os.makedirs(path)
            print('创建了文件夹：meizitu')
        if method == 'all':
            url = self.url_all
        elif method == 'old':
            url = self.url_old
        time.sleep(1)
        html = self.http.request('GET', url, headers=self.headers)
        hrefs = re.findall(': <a href="(.*?)" target="_blank">.*?</a>', html.data.decode())
        tits = re.findall(': <a href=".*?" target="_blank">(.*?)</a>', html.data.decode())
        for href, tit in zip(hrefs[start_page:], tits[start_page:]):
            self.check_dirs(tit)
            self.add_picture_list(href)
            for picture in self.picture_list:
                real_url = self.find_real_url(picture)
                filemane = real_url[-8:-4]
                flag = self.check_picture(filemane)
                if flag:
                    print('图片：%s.jpg 已存在' % filemane)
                else:
                    headers = {
                        'User-Agent': random.choice(self.useragents),
                        'Referer': picture
                    }
                    time.sleep(random.randint(1, 2))
                    response = self.http.request('GET', real_url, headers=headers)
                    self.save_picture(filemane, response.data)
            os.chdir('E:/meizitu/')

    # 检查文件夹
    def check_dirs(self, name):
        path = os.path.join('E:/meizitu/', name)
        if not os.path.exists(path):
            os.makedirs(path)
            print('创建了文件夹：%s' % name)
        else:
            print('文件夹：%s 已存在' % name)
        os.chdir(path)

    # 检查图片是否存在
    def check_picture(self, name):
        path = os.path.join('./', name + '.jpg')
        if os.path.exists(path):
            return True
        else:
            return False

    # 获取最大页面数量
    def find_max_span(self, url):
        time.sleep(random.randint(0, 1))
        html = self.http.request('GET', url, headers=self.headers)
        max_span = re.findall('<span>(.*?)</span></a>', html.data.decode())
        return int(max_span[-2])

    # 添加带下载图片地址至待下载图片地址列表
    def add_picture_list(self, url):
        self.picture_list = []
        span = self.find_max_span(url)
        for i in range(1, span + 1):
            picture_url = '%s/%s' % (url, str(i))
            self.picture_list.append(picture_url)

    # 获取真实下载页面
    def find_real_url(self, url):
        time.sleep(random.randint(1, 2))
        html = self.http.request('GET', url, headers=self.headers)
        picture_href = re.findall('<img src="(.*?)" alt=".*?"', html.data.decode())
        return picture_href[0]

    # 保存图片，输出消息
    def save_picture(self, file_name, sourse):
        with open(file_name + '.jpg', 'ab') as f:
            f.write(sourse)
        print('成功下载图片：%s' % file_name)


if __name__ == '__main__':
    meizitu = Meizitu()
    meizitu.start(start_page=26)
