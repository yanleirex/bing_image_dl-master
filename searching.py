#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import time
import json
import types
import logging

import requests

from redis_queue import RedisQueue


class Searcher(object):
    def __init__(self, engine_name):
        self.sess = requests.Session()
        self.engine_name = engine_name
        self.queue = RedisQueue('image_url')
        self.page_count = 35
        self.wait_second = 0

    @staticmethod
    def _convert_response(response):
        if response:
            content_type = response.headers['content-type']
            if content_type == 'application/json':
                return response.json()
            else:
                return response.content

    def wait(self, wait_second):
        self.wait_second = wait_second

    def do_search(self, key_word):
        """Search key word and push urls into redis queue
        :param key_word: key_words you want to search.
        :type key_word: str
        """

        current_page = 0
        logging.info("Searching key word: %s" % key_word)
        last_url = ''
        while True:
            resp = self._build_search_request(key_word, current_number=current_page)
            urls = self._parse_search_result(resp=resp)
            try:
                if urls[-1] == last_url:
                    break
                last_url = urls[-1]
                for url in urls:
                    url_item = {
                        'key_word': key_word,
                        'image_url': url
                    }
                    # self.queue.put(url_item)
                    self.queue.set_add(item=url_item)
                    logging.info('Store into redis "{0}":"{1}"'.format(key_word, url))
                current_page += self.page_count
                if self.wait_second:
                    logging.info('Waiting 10 seconds')
                    time.sleep(self.wait_second)
            except IndexError:
                logging.info('FAILED: No search result for {0}'.format(key_word))
                break

    def _download_html(self, url):
        """Download html of url
        :param url: url to download
        :type url: string"""
        resp = self.sess.get(url)
        if resp.status_code == 200:
            return resp
        else:
            return None

    def _build_search_request(self, key_word, current_number=0):
        """Build search request
        :param key_word:which key word to search
        :param current_number: which page to search
        """
        base_url = ''
        params = dict()
        if self.engine_name == 'baidu':
            base_url = 'http://image.baidu.com/search/index/acjson'
            params = {
                'tn': 'resultjson_com',
                'ipn': 'rj',
                'queryWord': key_word,
                'word': key_word,
                'pn': current_number,
                'rn': '30',
                'ie': 'utf-8',
                'fp': 'result',
                'ct': '201336592'
            }

        elif self.engine_name == 'bing':
            base_url = 'http://cn.bing.com/images/async'
            params = {
                'q': key_word,
                'async': 'content',
                'first': str(current_number),
                'count': self.page_count,
            }
        logging.info('Request searching url: {0}'.format(base_url))
        resp = self.sess.get(base_url, params=params)
        return Searcher._convert_response(resp)

    def _parse_search_result(self, resp):
        """Get image url from response
        :param resp: response of request
        """
        urls = []
        # if type(resp) is types.StringType:
        if isinstance(resp, types.StringType):
            if self.engine_name == 'baidu':
                results = json.loads(resp)['data']
                for result in results:
                    urls.append(result['thumbURL'])
            if self.engine_name == 'bing':
                urls = re.findall('imgurl:&quot;(.*?)&quot;', resp)
        return urls


if __name__ == "__main__":
    searcher = Searcher('bing')
    searcher.do_search('sweet william')
