# -*- coding: utf-8 -*-

import configparser
import json
from os import listdir

import jieba
import pymongo


class Doc:
    doc_id = 0
    tf = 0
    ld = 0

    def __init__(self, doc_id, tf, ld):
        self.doc_id = doc_id
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return str(self.doc_id) + '\t' + str(self.tf) + '\t' + str(self.ld)

    def __str__(self):
        return str(self.doc_id) + '\t' + str(self.tf) + '\t' + str(self.ld)


class IndexModule:
    stop_words = set()
    postings_lists = list()

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
            if not i:
                continue
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    def save_postings_to_db(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        connection = pymongo.MongoClient(config['DEFAULT']['host'], int(config['DEFAULT']['port']))
        db_name = config['DEFAULT']['DBName']
        db = connection[db_name]
        for posting in self.postings_lists:
            db['movie'].insert(posting, check_keys=False)

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        files = listdir(config['DEFAULT']['doc_dir_path'])
        avg_l = 0
        for i in files:
            with open(config['DEFAULT']['doc_dir_path'] + i, 'r', encoding='utf-8') as f:
                root = json.load(f)
                doc_id = int(root['id'])
                title = root['title']
                ename = root['ename']
                types = root['types']
                img = root['img']
                body = root['body'][0:120] + '...'
                directors = root['directors']
                actors = root['actors']
                seg_list = jieba.lcut(title + '.' + body + '.' + ename + '.' + types + '.' + directors + '.' + actors,
                                      cut_all=False)
                ld, cleaned_dict = self.clean_list(seg_list)
                avg_l = avg_l + ld
                for key, value in cleaned_dict.items():
                    d = {'id': doc_id, 'title': title, 'ename': ename, 'types': types, 'img': img,
                         'body': body, 'directors': directors, 'actors': actors}
                    for posting in self.postings_lists:
                        if posting['key'] == key:
                            posting['docs'] = d
                            posting['df'] = posting['df'] + 1
                            continue
                    p = {'key': key, 'df': 1, 'tf': value, 'ld': ld, 'docs': d}
                    self.postings_lists.append(p)
        avg_l = avg_l / len(files)
        config.set('DEFAULT', 'N', str(len(files)))
        config.set('DEFAULT', 'avg_l', str(avg_l))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configfile:
            config.write(configfile)
        self.save_postings_to_db()


if __name__ == '__main__':
    im = IndexModule('statics/config.ini', 'utf-8')
    im.construct_postings_lists()
