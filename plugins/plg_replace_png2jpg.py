import utilforplgs as ufp
import os
import re
import sys

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]

"""
jpgをpngにする
"""


def translate(img_pass):
    img = ufp.my_imread(img_pass)
    base, ext = os.path.splitext(img_pass)
    # cv2.imshow("aa",img)
    ufp.my_imwrite(base + ".jpg", img)
    os.remove(img_pass)


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)

    for i, sep in enumerate(aldf):
        if re.search(r".*\.(jp.?g|webp|bmp|png)", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                translate(sep)
                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
