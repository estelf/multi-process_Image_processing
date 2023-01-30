import glob
import os
import re
import sys
import time

import cv2
import numpy as np

"""
ハッシュmd5名でリネームする
"""
args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_GRAYSCALE)
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
                img = my_imread(sep)
                if img is None:
                    break

                img = cv2.blur(img, (11, 11))
                # ###-------------------------------------### #
                img2 = cv2.Laplacian(img, cv2.CV_32F, ksize=5).var()

                _, ext = os.path.splitext(sep)
                tem = 0
                while True:
                    try:
                        # print(f"{img2}_{tem}{ext}")
                        os.rename(sep, f"{img2}_{tem}{ext}")
                        break
                    except FileExistsError:
                        tem = tem + 1
                # ###-------------------------------------####

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
try:
    main(starts, step, flname)
except Exception as e:
    with open(f"{starts}_error.txt", "w") as f:
        f.write(str(e))
# end_time = time.perf_counter()

# 経過時間を出力(秒)
# elapsed_time = end_time - start_time
# print(elapsed_time,"秒")
