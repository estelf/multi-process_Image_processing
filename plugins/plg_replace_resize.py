import cv2
import utilforplgs as ufp
import os
import sys
import re

args = sys.argv

starts = int(args[3])
step = int(args[2])
flname = args[1]
"""
256にリサイズ(このまま)
"""


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)

    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = ufp.my_imread(sep)
                # ###-------------------------------------####
                img = cv2.resize(img, (256, 256))
                ufp.my_imwrite(sep, img)
                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
