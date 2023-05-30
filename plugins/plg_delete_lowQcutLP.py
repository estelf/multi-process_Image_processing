import utilforplgs as ufp
import os
import re
import sys
import imutils
import cv2

"""
ハッシュmd5名でリネームする
"""
args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                img = ufp.my_imread(sep)

                if img is None:
                    break
                else:
                    height, width, ch = img.shape
                    if width > 256:
                        img = imutils.resize(img, width=256)
                    elif height > 256:
                        img = imutils.resize(img, height=256)

                img = cv2.bilateralFilter(img, 9, 75, 75)
                img = cv2.bilateralFilter(img, 9, 75, 75)
                img = cv2.bilateralFilter(img, 9, 75, 75)
                # ###-------------------------------------### #
                img2 = cv2.Laplacian(img, cv2.CV_32F, ksize=5).var()

                if img2 < 14000:
                    os.remove(sep)

                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
