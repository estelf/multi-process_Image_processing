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
# 指定した画像(path)の物体を検出し、外接矩形の画像を出力します


def detect_contour(path):

    # 画像を読込
    src = my_imread(path)
    # src = src[:, 110:, :]
    # グレースケール画像へ変換
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = cv2.Laplacian(src, -1, ksize=5)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    # 2値化
    retval, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 輪郭を抽出
    #   contours : [領域][Point No][0][x=0, y=1]
    #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
    #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
    contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 矩形検出された数（デフォルトで0を指定）

    x1, y1 = 9999999, 99999999
    x2, y2 = 0, 0

    # 各輪郭に対する処理
    for i in range(0, len(contours)):

        # 輪郭の領域を計算
        area = cv2.contourArea(contours[i])

        # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
        if area < 1e2 or 1e5 < area:
            continue

        # 外接矩形
        if len(contours[i]) > 0:
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)
            # cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if x < x1:
                x1 = x
            if y < y1:
                y1 = y

            if x + w > x2:
                x2 = x + w
            if y + h > y2:
                y2 = y + h

    cv2.rectangle(src, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 外接矩形された画像を表示
    # cv2.imshow("output", src)
    # cv2.waitKey(0)

    # 終了処理
    cv2.destroyAllWindows()
    h, w, _ = src.shape
    # print(f"{0} {(x2 + x1) / (2 * w)} {(y2 + y1) / (2 * h)} {(x2 - x1) / w} {(y2 - y1) / h}")
    return f"{0} {(x2 + x1) / (2 * w)} {(y2 + y1) / (2 * h)} {(x2 - x1) / w} {(y2 - y1) / h}"


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

    os.makedirs("label", exist_ok=True)
    with open("label\\classes.txt", "w") as f:
        f.write("umamusume")

    aldf = glob.glob("*.*")
    time.sleep(1)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # ###-------------------------------------### #
                a = detect_contour(sep)
                with open("label\\" + sep[:-3] + "txt", "w") as f:
                    f.write(a)
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
