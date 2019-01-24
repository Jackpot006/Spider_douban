import requests
import json
import re
import pymongo
from requests import RequestException
from config import *
from bs4 import BeautifulSoup

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_one_page(url,headers):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # pattern = re.compile('.*?"rating":\["(.*?)",.*?"rank":(\d+).*?"cover_url":"(.*?)".*?"id":"(.*?)".*?"types":(.*?)"regions":(.*?)title":"(.*?)".*?"url":"(.*?)".*?"release_date":"(.*?)".*?"vote_count":(.*?),"score".*?"actors":(.*?),"is_watched":false.*?',re.S)
    # items = re.findall(pattern,html)
    # for item in items:
    #     yield {
    #         'ratings':item[0].strip(),
    #         'rank':item[1].strip(),
    #         'img':item[2].replace('\\','').strip(),
    #         'id':item[3].strip(),
    #         'types':item[4].replace('[','').replace(']','').replace('"','').replace(',',' ').strip(),
    #         'regions':item[5].replace('[','').replace(']','').replace('"','').replace(',',' ').strip(),
    #         'title':item[6].strip(),
    #         'url':item[7].replace('\\','').strip(),
    #         'date':item[8].strip(),
    #         'comments':item[9].strip(),
    #         'actors':item[10].replace('[','').replace(']','').replace('"','').replace(',',' ').strip()
    #     }
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('#content > div.sreach_div > div:nth-child(1) > h3 > a')
    for t in title:
        print(t.text)

def write_to_file(content):
    with open('doubanMovies.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close

def save_to_mongo(data):
    if db[MONGO_TABLE].update({'id':data['id']},{'$set':data},True):
        print('Saved to Mongo',data)
    else:
        print('Saved to Mongo Failed',data)

def main(pageNo):
    global url
    url = 'http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22cdr%22%3A%22AND%22%2C%22cds%22%3A%5B%7B%22fld%22%3A%22title%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E5%9C%B0%E9%9C%87%22%7D%2C%7B%22fld%22%3A%22subTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E5%9C%B0%E9%9C%87%22%7D%2C%7B%22fld%22%3A%22introTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E5%9C%B0%E9%9C%87%22%7D%2C%7B%22fld%22%3A%22contentText%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E5%9C%B0%E9%9C%87%22%7D%5D%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&ss=1&pageSize=20'+'&pageNo='+str(pageNo)
    headers = {
        'Accept': '* / *',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
    }
    html = get_one_page(url,headers)
    # for item in parse_one_page(html):
    #     # write_to_file(item)
    #     save_to_mongo(item)
    parse_one_page(html)

if __name__ == '__main__':
    # for i in range(30):
    #     main(i*20,MAX_PAGE,TYPE)
    global url
    # for type in range(1,31):
    #     for page in (10,9,8,7,6,5,4,3,2,1):
    #         for s in range(30):
    #             main(s*20,page*10,type)
    #             print('Now calling: ', url)
    for i in range(1,10):
        main(i)