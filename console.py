# -*- coding:utf-8 -*-
# Created by yanlei on 16-9-20 at 上午10:25

from __future__ import division
import glob
import time
import os
import redis


def check_status(r):
    old_total_files = 0
    while True:
        info = r.info()
        keys = r.keys()
        num_of_keys = []
        for key in keys:
            num_of_keys.append(r.scard(key))
        num_of_jpg = len(glob.glob('*/*.jpg'))
        num_of_JPG = len(glob.glob('*/*.JPG'))
        num_of_png = len(glob.glob('*/*.png'))
        num_of_PNG = len(glob.glob('*/*.PNG'))
        num_of_jpeg = len(glob.glob('*/*.jpeg'))
        num_of_JPEG = len(glob.glob('*/*.JPEG'))
        num_of_gif = len(glob.glob('*/*.gif'))
        num_of_GIF = len(glob.glob('*/*.GIF'))
        num_of_bmp = len(glob.glob('*/*.bmp'))
        num_of_BMP = len(glob.glob('*/*.BMP'))
        num_of_tiff = len(glob.glob('*/*.tiff'))
        num_of_TIFF = len(glob.glob('*/*.TIFF'))
        i = os.system('clear')
        print "--------------Download Statistics---------------"
        print "Number of jpg:  ", num_of_jpg
        print "Number of JPG:  ", num_of_JPG
        print "Number of png:  ", num_of_png
        print "Number of PNG:  ", num_of_PNG
        print "Number of jpeg: ", num_of_jpeg
        print "Number of JPEG: ", num_of_JPEG
        print "Number of gif:  ", num_of_gif
        print "Number of GIF:  ", num_of_GIF
        print "Number of bmp:  ", num_of_bmp
        print "Number of BMP:  ", num_of_BMP
        print "Number of tiff: ", num_of_tiff
        print "Number of TIFF: ", num_of_TIFF
        print "Total images:   ", num_of_jpg + num_of_JPG + num_of_png + num_of_PNG + num_of_jpeg + num_of_JPEG + num_of_gif + num_of_GIF + num_of_bmp + num_of_BMP + num_of_tiff + num_of_TIFF
        total_files = len(glob.glob('*/*.*'))
        print "Total files:    ", total_files
        print "Download speed: {0} files/s".format((total_files - old_total_files))
        print "--------------Redis Statistics-------------------"
        print "All key:"
        for ii in range(len(keys)):
            print keys[ii], ": ", num_of_keys[ii]
        old_total_files = total_files
        print "used memory: ", info['used_memory_human']
        print "connected clients: ", info['connected_clients']
        print "total commands processed: ", info['total_commands_processed']
        time.sleep(1)

if __name__ == "__main__":
    r_c = redis.Redis('192.168.0.201', 6379)
    check_status(r_c)
