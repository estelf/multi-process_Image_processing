"""
面積が256の二乗以下もしくはh,wが200px以下の画像を削除する

"""
import cv2
import numpy as np
import glob
import os
import sys
import time
import re

args = sys.argv

starts = int(args[3])
step = int(args[2])
flname = args[1]


def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(e)
        return None


def main(starts, step, flname):
    os.chdir(flname)
    aldf = glob.glob("*.*")
    time.sleep(1)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # print(i,starts,step)
                img = my_imread(sep)
                # ###-------------------------------------####
                h, w, _ = img.shape
                if h * w < 256**2 or (h < 200 and w < 200):
                    os.remove(sep)

                # ###-------------------------------------####

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
# end_time = time.perf_counter()

# 経過時間を出力(秒)
# elapsed_time = end_time - start_time
# print(elapsed_time,"秒")
