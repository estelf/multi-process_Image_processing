"""
プラグイン用便利クラス
"""
import cv2
import os
import numpy as np
import traceback


def my_imread(filename, readtype=cv2.IMREAD_COLOR):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, readtype)

        if len(list(img.shape)) != 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        return img
    except Exception as e:
        print(e)
        print(traceback.format_exc())
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
        print(traceback.format_exc())
        return False


def filereader(filename="master.csv"):
    with open(filename, "r", encoding="utf-8") as f:
        a = [i.strip() for i in f.readlines()]
    return a


def Trace2file(num):
    """エラー検知でこれーた"""

    def _Trace2file(funk):
        def wrapper(*args):
            try:
                funk(*args)
            except Exception as e:
                with open(f"{num}_error.txt", "w", encoding="utf-8") as f:
                    print(str(e) + "\n---\n" + str(traceback.format_exc()))
                    f.write(str(e) + "\n---\n" + str(traceback.format_exc()))

        return wrapper

    return _Trace2file
