import glob
import os
import re
import sys

import cv2
import numpy as np

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]

"""
jpgをpngにする
"""


def translate(img_pass):
    img = my_imread(img_pass)
    base, ext = os.path.splitext(img_pass)
    # cv2.imshow("aa",img)
    my_imwrite(base + ".png", img)
    os.remove(img_pass)


# note 26702


def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(e)
        return None


def my_imwrite(filename, img):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img)
        if result:
            with open(filename, mode="w+b") as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def main(starts, step, flname):
    os.chdir(flname)
    for i, sep in enumerate(glob.glob("*.*")):
        if re.search(r".*\.(jp.?g|webp|bmp)", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # print(i,starts,step)
                translate(sep)
                # ###-------------------------------------####

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
# end_time = time.perf_counter()
