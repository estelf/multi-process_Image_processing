import utilforplgs as ufp
import os
import re
import shutil
import sys

import dlib


args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


def detect_dlib(image):
    face_detector = dlib.simple_object_detector("../detector_face.svm")

    # 顔の検出
    faces = face_detector(image)
    a = [[(rect.left(), rect.top()), (rect.right(), rect.bottom())] for rect in faces]
    return a


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    os.makedirs("OK", exist_ok=True)
    os.makedirs("NG", exist_ok=True)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = ufp.my_imread(sep)

                # ###-------------------------------------####
                # #print(sep)

                faces2 = detect_dlib(img)
                if len(faces2) > 0:
                    shutil.move(sep, "OK")
                else:
                    shutil.move(sep, "NG")
                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
