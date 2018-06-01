# -*- coding: utf-8 -*-

import configparser
import urllib.request
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


def crawl_movies(doc_dir_path, doc_encoding):
    path = 'https://maoyan.com'
    j = 1
    for i in range(27318):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/66.0.3359.139 Safari/537.36',
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
            ET.SubElement(doc, "body").text = body
            tree = ET.ElementTree(doc)
            tree.write(doc_dir_path + "%d.xml" % j, encoding=doc_encoding, xml_declaration=True)
            print(j)
            j += 1


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('statics/config.ini', 'utf-8')
    crawl_movies(config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
