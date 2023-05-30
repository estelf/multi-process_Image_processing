"""
クオリティの低いデータを計算し削除する拡張機能

"""
import utilforplgs as ufp
import os
import re
import sys
import shutil


args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    os.makedirs("errorFile", exist_ok=True)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = ufp.my_imread(sep)
                if img is None:
                    shutil.move(sep, "errorFile")
                # ###-------------------------------------### #

    os.chdir("..")


main(starts, step, flname)
