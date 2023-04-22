# 文件夹中每个文件都进行压缩
# -*- coding: utf-8 -*-
import tkinter.filedialog
from tqdm import tqdm
import os
from osgeo import gdal
import time
from os.path import *
import PySimpleGUI as sg
import threading

thread_count = 4

# 数组分割
def arr_size(arr, size):
    # size为被分成的子数组的元素个数
    s = []
    for i in range(0, int(len(arr)) + 1, size):
        c = arr[i:i + size]
        s.append(c)
    newlist = [x for x in s if x]
    return newlist


def get_file_size(file_path):
    """获取文件占空间所少M"""
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def progress(percent, msg, tag):
    """进度回调函数"""
    print(percent, msg, tag)
    # sg.one_line_progress_meter("进度", int(percent * 100), 100)


def compress(path, target_path):
    """使用gdal进行文件压缩"""
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, callback=progress, options=["TILED=YES", "COMPRESS=LZW"])
    # strict=1表示和原来的影像严格一致，0表示可以有所调整
    # callback为进度回调函数
    # PACKBITS快速无损压缩，基于流
    # LZW针对像素点，黑白图像效果好
    del dataset


filename = tkinter.filedialog.askopenfilenames(title='选择tif文件', filetypes=[('tif', '*.tif'), ('All Files', '*')],
                                               initialdir='C:\\Windows\\WsdlFile')


class MyThread(threading.Thread):
    def __init__(self, path, target_path):
        threading.Thread.__init__(self)
        self.path = path
        self.target_path = target_path

    def run(self):
        compress(self.path, self.target_path)


def group_processd(in_file_list):
    threads = []
    for item in in_file_list:
        threads.append(MyThread(item[0],item[1]))
    for t in threads:  # 开启线程
        t.start()
    for t in threads:  # 阻塞线程
        t.join()
    return 0


# 压缩函数
all_task = []
print("start grouping")
for i in tqdm(range(len(filename))):
    all_task.append([filename[i], join(dirname(filename[i]), "ZIP.{}".format(basename(filename[i])))])
group_all_task = arr_size(all_task, thread_count)
print("start processing")
for i in tqdm(range(len(group_all_task))):
    print(group_all_task[i])
    group_processd(group_all_task[i])
# for i in tqdm(range(len(filename))):
#     print("path", filename[i])
#     target_path = join(dirname(filename[i]), "ZIP.{}".format(basename(filename[i])))
#     print("target_path", target_path)
#     compress(filename[i], target_path)
