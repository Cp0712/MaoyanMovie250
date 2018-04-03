import json
import re
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool

#获取一个url下的html文件
def get_one_page(url):
    try:
        #添加请求头
        headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求失败')
        return None
    except RequestException:
        return None

#使用正则解析html文件
def parse_one_page(html):
    #如果不加re.S(任意匹配)  .就不会匹配换行符!
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)" alt="(.*?)" class="board-img" />.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:  #构造一个生成器可以使用for遍历
        #生成一个字典
        yield{
            'index' : item[0],
            'image': item[1],
            'title': item[2],
            #strip()去除空格和\n  切片去除  主演:
            'actor': item[3].strip()[3:],
            'time' : item[4].strip()[5:],
            'score' : item[5]+item[6]
        }

#写入文件 使用json加载字典
def write_to_file(content):
    #加上encoding='utf-8'  和  ensure_ascii=False显示汉字
    with open('多进程.txt', 'a', encoding='utf-8') as f:
        #字典转换成字符串
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

#主函数运行
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])