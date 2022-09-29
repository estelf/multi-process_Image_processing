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


def resize_img(img):
    """
    画像をpaddingし

    """
    try:
        height, width, _ = img.shape  # 画像の縦横サイズを取得
    except Exception:
        height, width = img.shape

    diffsize = abs(height - width)
    padding_half = int(diffsize / 2)

    # 縦長画像→幅を拡張する
    if height > width:
        padding_img = cv2.copyMakeBorder(
            img, 0, 0, padding_half, height - (width + padding_half), cv2.BORDER_REFLECT
        )
    # 横長画像→高さを拡張する
    elif width > height:
        padding_img = cv2.copyMakeBorder(
            img, padding_half, width - (height + padding_half), 0, 0, cv2.BORDER_REFLECT
        )
    else:
        padding_img = img
    return padding_img


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
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # print(i,starts,step)
                img = my_imread(sep)

                # ###-------------------------------------### #
                img = resize_img(img)
                my_imwrite(sep, img)
                # ###-------------------------------------### #

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
# end_time = time.perf_counter()

# 経過時間を出力(秒)
# elapsed_time = end_time - start_time
# print(elapsed_time,"秒")
