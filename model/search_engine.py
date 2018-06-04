# -*- coding: utf-8 -*-

import configparser
import math
import operator

import jieba
import pymongo


class SearchEngine:
    stop_words = set()
    config_path = ''
    config_encoding = ''
    K1 = 0
    B = 0
    N = 0
    avg_l = 0
    conn = None

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.conn = pymongo.MongoClient(config.get('DB', 'host'), int(config.get('DB', 'port')))
        db_name = config.get('DB', 'DBName')
        self.db = self.conn[db_name]
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])

    def __del__(self):
        self.conn.close()

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

    def fetch_from_db(self, term):
        return self.db['movie'].find(term)

    def result_by_BM25(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r['df']
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            doc = r['doc']
            tf = doc['tf']
            ld = doc['ld']
            docid = doc['doc_id']
            s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
            if docid in BM25_scores:
                BM25_scores[docid] = BM25_scores[docid] + s
            else:
                BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key=operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def search(self, sentence):
        return self.result_by_BM25(sentence)

    def searchidlist(self, key):
        global page
        global doc_id
        se = SearchEngine('statics/config.ini', 'utf-8')
        flag, id_scores = se.search(key)
        # 返回docid列表
        doc_id = [i for i, s in id_scores]
        page = []
        for i in range(1, (len(doc_id) // 10 + 2)):
            page.append(i)
        return flag, page


if __name__ == "__main__":
    se = SearchEngine('statics/config.ini', 'utf-8')
