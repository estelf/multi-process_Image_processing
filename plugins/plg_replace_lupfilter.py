import utilforplgs as ufp
import os
import re
import sys

import cv2


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
                # #print(i,starts,step)
                img = ufp.my_imread(sep)

                # ###-------------------------------------### #
                img = cv2.Laplacian(img, cv2.CV_32F, ksize=5)
                ufp.my_imwrite(sep, img)
                # ###-------------------------------------### #

    os.chdir("..")


main(starts, step, flname)
