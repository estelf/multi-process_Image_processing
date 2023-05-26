import utilforplgs as ufp
import os
import re
import shutil
import sys

import cv2
import dlib


args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]

"""
顔がある画像を"face"フォルダに入れる
"""


def translate(img_pass):
    img = ufp.my_imread(img_pass)
    base, ext = os.path.splitext(img_pass)
    # cv2.imshow("aa",img)
    ufp.my_imwrite(base + ".png", img)
    os.remove(img_pass)


# note 26702


@ufp.Trace2file(starts)
def main(starts, step, flname):
    detector = dlib.get_frontal_face_detector()  # cnn_face_detection_model_v1 also can be used
    aldf = ufp.filereader()
    os.chdir(flname)
    os.makedirs("face", exist_ok=True)

    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = ufp.my_imread(sep)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = detector(img, 1)
                if len(dets) > 0:
                    shutil.move(sep, "face")
                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
