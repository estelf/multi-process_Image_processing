"""
クオリティの低いデータを計算し削除する拡張機能

"""
import glob
import os
import re
import sys

import cv2
import numpy as np
import time

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]
model_path = "..\\brisque_model_live.yml"  # BRISQUEモデルデータ
range_path = "..\\brisque_range_live.yml"  # BRISQUE範囲データ


def filereader():
    with open("master.csv", "r", encoding="utf-8") as f:
        a = [i.strip() for i in f.readlines()]
    return a


def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(e)
        return None


def main(starts, step, flname):
    aldf = filereader()
    os.chdir(flname)

    time.sleep(1)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # print(i,starts,step)
                img = my_imread(sep)
                # ###-------------------------------------### #
                score1 = cv2.quality.QualityBRISQUE_compute(img, model_path, range_path)

                # print(score1[0])  #スコア表示させたいときだけ

                if score1[0] > 47:  # 数値を変えるだけ
                    os.remove(sep)

                # ###-------------------------------------### #

    os.chdir("..")


# start_time = time.perf_counter()
try:
    main(starts, step, flname)
except Exception as e:
    with open(f"{starts}_error.txt", "w") as f:
        f.write(str(e))
    exit(1)
# end_time = time.perf_counter()

# 経過時間を出力(秒)
# elapsed_time = end_time - start_time
# print(elapsed_time,"秒")
