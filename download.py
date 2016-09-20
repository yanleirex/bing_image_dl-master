#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
import multiprocessing

import requests

from redis_queue import RedisQueue


class Downloader(object):
    """Simple downloader to download image url from redis queue"""
    def __init__(self, path_dir):
        """Connect to redis, and init requests session"""
        self.url_queue = RedisQueue('image_url')
        self.failed_url_queue = RedisQueue('failed_image_url')
        self.downloaded_url_queue = RedisQueue('downloaded_image_url')
        self.sess = requests.Session()
        self.path_dir = os.path.join(os.getcwd(), path_dir)

    def _do_request(self, url_item):
        """request a image url, return response"""
        if url_item:
            url = url_item['image_url']
            # key_word = url_item['key_word']
            resp = self.sess.get(url)
            if resp.status_code is 200:
                logging.info("Request image url: {0}".format(url))
                return resp.content
            else:
                self.failed_url_queue.set_add(url_item)
                logging.error("Request {0} failed!".format(url))
                return None
        else:
            logging.error("No image url")
            return None

    def _do_download(self, url_item):
        """Write response(image) to disk"""
        url_item = eval(url_item)
        if url_item:
            key_word = url_item['key_word']
            url = url_item['image_url']
            if not self.downloaded_url_queue.set_is_member(url):
                image_name = os.path.split(url)[-1]
                file_path = self.path_dir + '/' + key_word.replace(' ', '_')
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_name = file_path + '/' + image_name
                # if not file_name.lower().endswith('.jpg'):
                #     file_name += '.jpg'
                # if len(file_name) > 40:
                #     file_name = file_name[:36] + file_name[-4]
                try:
                    content = self._do_request(url_item)
                    if content:
                        with open(file_name, 'wb') as f:
                            f.write(content)
                            logging.info("Download {0}".format(url))
                            self.downloaded_url_queue.set_add(url)
                except Exception as e:
                    logging.error(e)
        else:
            logging.error("No url item")

    def download(self):
        """Download function"""
        while True:
            if not self.url_queue.set_empty():
                url_item = self.url_queue.set_pop()
                self._do_download(url_item)
            elif not self.failed_url_queue.set_empty():
                url_item = self.failed_url_queue.set_pop()
                self._do_download(url_item)
            else:
                logging.error("No image urls to download")
                continue

if __name__ == "__main__":
    downloader = Downloader('bing')
    jobs = []
    for i in range(32):
        p = multiprocessing.Process(target=downloader.download)
        jobs.append(p)
        p.start()
