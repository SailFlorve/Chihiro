# -*- coding: utf-8 -*-

import configparser
import random
import urllib.request
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

user_agent_list = [
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW6s4; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; yie8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; Zune 3.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; MS-RTC LM 8; Zune 4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
    ]

def crawl_movies(doc_dir_path, doc_encoding):
    path = 'https://maoyan.com'
    j = 1
    for i in range(27318):
        try:
            headers = {'User-Agent': random.choice(user_agent_list),
                       'Cookie': 'uuid=1A6E888B4A4B29B16FBA1299108DBE9CE4B584628BAA0D9413EC30D0C831E00D;'
                                ' _lxsdk_cuid=162cbe8c4ebc8-017a879b6bf7b8-b34356b-1fa400-162cbe8c4ebc8;'
                                ' iuuid=3359B574C6E001EC71AF8553E6DA5A93B872F20693493FAB44F448EA9A082B8C;'
                                ' _csrf=3a0e9165fd4bf1f33c96d553a1cc8ed607035b4d13b79c3ebde6f60b5f7df1a6;'
                                ' _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic;'
                                ' _lxsdk=3359B574C6E001EC71AF8553E6DA5A93B872F20693493FAB44F448EA9A082B8C;'
                                ' lt=A__uzLbjUf9iTse7vBuAwu-m7cQAAAAA3QUAADeX0uvyBwiImwoS7KYR-PgqOocXUch27'
                                'wfHxLO6iLwlC3n-cxpJE6jXYjJhQi74kA; lt.sig=dvtT0ZM2Casq24WHTPqGO9FqrG4;'
                                ' __mta=217824553.1523839453033.1526261741167.1526261912275.13;'
                                ' _lxsdk_s=1635c2c05c7-f02-5a6-008%7C%7C24'}
            request = urllib.request.Request(url='https://maoyan.com/films?offset=' + str(30*i), headers=headers)
            response = urllib.request.urlopen(request)
        except Exception as e:
            print('----%s:%s----' % e, 'https://maoyan.com/films?offset=' + str(30*i))
            return
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find('dl', class_='movie-list').find_all('dd')
        for item in items:
            name = item.find('div', class_='channel-detail movie-item-title').get('title')
            url = path + item.find('div', class_='movie-item').find('a').get('href')
            img = item.find('div', class_='movie-poster').find_all('img')[1].get('data-src')
            doc = ET.Element("doc")
            ET.SubElement(doc, "id").text = "%d" % j
            ET.SubElement(doc, "url").text = url
            ET.SubElement(doc, "title").text = name
            ET.SubElement(doc, "img").text = img
            try:
                request_detail = urllib.request.Request(url=url, headers=headers)
                response_detail = urllib.request.urlopen(request_detail)
            except Exception as e:
                print(e)
                return
            html_detail = response_detail.read().decode('utf-8')
            soup_detail = BeautifulSoup(html_detail, 'lxml')
            body = soup_detail.find('span', class_='dra').string
            directors = list()
            for s in soup_detail.find('div', class_='tab-desc tab-content active').find_all('li', class_='celebrity '):
                directors.append(str(s.find('div', class_='info').find('a').string).strip())
            actors = list()
            for s in soup_detail.find('div', class_='tab-desc tab-content active').find_all('li', class_='celebrity actor'):
                actors.append(str(s.find('div', class_='info').find('a').string).strip())
            ET.SubElement(doc, "body").text = body
            ET.SubElement(doc, "directors").text = '.'.join(directors)
            ET.SubElement(doc, "actors").text = '.'.join(actors)
            tree = ET.ElementTree(doc)
            tree.write(doc_dir_path + "%d.xml" % j, encoding=doc_encoding, xml_declaration=True)
            print(j)
            j += 1


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('statics/config.ini', 'utf-8')
    crawl_movies(config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
