import requests
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool

url = 'http://www.ip181.com/'
headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}


def get_html():
    try:
        proxies = {'http': 'http://122.138.183.203:8118'}
        response = requests.get('http://www.ip181.com/', headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text

        return None
    except requests.ConnectionError:
        print("连接出错")
        return None


def get_ip(html):
    #    soup=BeautifulSoup(html,'lxml')
    #    ip=soup.find_all('body > div:nth-child > div.panel.panel-info > div.panel-body > div > div:nth-child > table > tbody > tr.active ')
    pattern = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>.*?<tr>', re.S)
    items = re.findall(pattern, html)
    for item in items[2:]:
        yield {
            'ip': item[0],
            'port': item[1]
        }


def save_ip(ip):
    proxy = []
    proxy.append(ip)

    proxies = {
        'http': 'http://' + proxy.pop()

    }
    # print(proxies)
    try:
        t1 = time.time()
        res = requests.get('http://www.baidu.com', proxies=proxies)
        t2 = time.time()
        if res.status_code == 200:
            return proxies
        return None
    except requests.ConnectionError:
        print("出错")
        return None


def multiple_process():
    counts = [
        (1, 16),
        (17, 32),
        (33, 48)
    ]
    pool = Pool(processes=3)
    for count in counts:
        pool.apply_async(save_ip, (count[0], count[1]))
        pool.close()
        pool.jion()


def main():
    html = get_html()
    #    print(html)
    all = get_ip(html)
    quick = []
    for ip in all:
        nor = ip['ip'] + ':' + ip['port']
        h = save_ip(nor)
        if h:  # {'http': 'http://183.56.131.87:3128'}]
            quick.append(h)
            print(quick)


if __name__ == '__main__':
    main()
