# -*- coding: utf-8 -*-

import configparser
import sqlite3
import xml.etree.ElementTree as ET
from os import listdir

import jieba


class Doc:
    doc_id = 0
    date_time = ''
    tf = 0
    ld = 0

    def __init__(self, doc_id, date_time, tf, ld):
        self.doc_id = doc_id
        self.date_time = date_time
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return str(self.doc_id) + '\t' + self.date_time + '\t' + str(self.tf) + '\t' + str(self.ld)

    def __str__(self):
        return str(self.doc_id) + '\t' + self.date_time + '\t' + str(self.tf) + '\t' + str(self.ld)


class IndexModule:
    stop_words = set()
    postings_lists = {}

    config_path = ''
    config_encoding = ''

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    def write_postings_to_db(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS postings''')
        c.execute('''CREATE TABLE postings
                     (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')
        for key, value in self.postings_lists.items():
            doc_list = '\n'.join(map(str, value[1]))
            t = (key, value[0], doc_list)
            c.execute("INSERT INTO postings VALUES (?, ?, ?)", t)
        conn.commit()
        conn.close()

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        files = listdir(config['DEFAULT']['doc_dir_path'])
        avg_l = 0
        for i in files:
            root = ET.parse(config['DEFAULT']['doc_dir_path'] + i).getroot()
            title = root.find('title').text
            body = root.find('body').text
            doc_id = int(root.find('id').text)
            date_time = root.find('datetime').text
            seg_list = jieba.lcut(title + '。' + body, cut_all=False)
            ld, cleaned_dict = self.clean_list(seg_list)
            avg_l = avg_l + ld
            for key, value in cleaned_dict.items():
                d = Doc(doc_id, date_time, value, ld)
                if key in self.postings_lists:
                    self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                    self.postings_lists[key][1].append(d)
                else:
                    self.postings_lists[key] = [1, [d]]  # [df, [Doc]]
        avg_l = avg_l / len(files)
        config.set('DEFAULT', 'N', str(len(files)))
        config.set('DEFAULT', 'avg_l', str(avg_l))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configfile:
            config.write(configfile)
        self.write_postings_to_db(config['DEFAULT']['db_path'])


if __name__ == '__main__':
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()
