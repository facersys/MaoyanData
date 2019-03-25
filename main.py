# -*- coding: utf-8 -*-

import os
import requests
from lxml import etree
from multiprocessing import Process, Lock
from collections import deque

USER_INFO_URL = 'https://maoyan.com/films/celebrity/{uid}'
USER_PHOTO_URL = 'https://maoyan.com/films/celebrity/ajax/photos/{uid}'
DATA_DIR = 'Z:/MaoyanData/{username}/{i}.jpg'

TARGET_LIST = deque(list(range(19086, 19114)))


class MaoyanSpider(Process):
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        self.lock = Lock()

    def get_name(self):
        """"获取名字"""
        response = requests.get(USER_INFO_URL.format(uid=self.uid))
        if response.status_code == 200:
            html = etree.HTML(response.text)
            try:
                username_cn = html.xpath(
                    "//p[@class='china-name cele-name']")[0].text.strip()
                username_en = html.xpath(
                    "//p[@class='eng-name cele-name']")[0].text.strip().lower().replace(" ", "-")
            except IndexError:
                return None
            return '{}_{}_{}'.format(self.uid, username_cn, username_en)

    def get_photo(self, username):
        """"获取照片"""
        response = requests.get(USER_PHOTO_URL.format(uid=self.uid))
        if response.status_code == 200:
            photos = response.json().get('photos')
            i = 0
            if not photos:
                return False
            else:
                for photo in photos:
                    i += 1
                    photo_url = photo.get('olink').replace(r"/w.h", "")
                    self.save_photo(photo_url, DATA_DIR.format(
                        username=username, i=i))
                return True

    def save_photo(self, url, filename):
        """"保存照片"""
        dirname = "/".join(filename.split('/')[:-1])
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print('[照片保存成功]:', url)

    def run(self):
        username = self.get_name()
        if username and self.get_photo(username):
            print('[成功] %s' % username)
        else:
            print('[失败] %s' % self.uid)


def main():
    while True:
        plist = []
        for i in range(10):
            p = MaoyanSpider(TARGET_LIST.pop())
            p.start()
            plist.append(p)

        for p in plist:
            p.join()


if __name__ == "__main__":
    main()
