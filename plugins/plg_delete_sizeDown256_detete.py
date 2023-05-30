"""
面積が256の二乗以下もしくはh,wが200px以下の画像を削除する

"""
import utilforplgs as ufp
import os
import sys
import re

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
                # ###-------------------------------------####
                h, w, _ = img.shape
                if h * w < 256**2 or (h < 200 and w < 200):
                    os.remove(sep)

                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
