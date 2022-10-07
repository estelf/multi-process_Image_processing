"""
kmeans法を用いて代表色名でリネームする
"""
import colorsys
import glob
import os
import re
import sys
import time
import cv2
import numpy as np

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


def make_filename(img, basename):
    name = ""
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    colors_tem = img.reshape(-1, 3)
    colors = []
    for i in colors_tem:
        if sum(i) > 240 * 3:
            continue
        # print(i)
        colors.append(i)
    colors = np.array(colors).reshape(-1, 3).astype(np.float32)

    ret, label, center = cv2.kmeans(colors, 4, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    arg_ce = [round(colorsys.rgb_to_hsv(i[2], i[1], i[0])[0] * 1000) for i in center]
    arg_ce.sort(reverse=True)
    for i in arg_ce:
        name = str(i)[0:4] + "_" + name

    # cv2.imwrite("color\\"+basename,make_rect(center,50))

    return name + basename


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

                # ###-------------------------------------### #
                try:
                    name = make_filename(img, sep)
                    os.rename(sep, name)
                except Exception:
                    pass
                # ###-------------------------------------### #

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
