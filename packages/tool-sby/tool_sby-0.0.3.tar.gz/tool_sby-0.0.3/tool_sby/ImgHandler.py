#!/usr/bin/python3
# -*- coding:utf-8 -*-
from urllib.request import urlretrieve
import os


class ImgHandler:
    img_dir = '/data/img/'
    mount_dir = '/infinityfs1/hivefiles/sobeyhive/bucket-k/kdimage_t/img/'

    @classmethod
    def download(cls, project, img_url, ip=''):
        if not os.path.exists(cls.img_dir + project):
            os.makedirs(cls.img_dir + project)
        path = img_url.split('/')[-1]
        urlretrieve(ip + img_url, cls.img_dir + project + '/' + path)
        return cls.mount_dir + project
