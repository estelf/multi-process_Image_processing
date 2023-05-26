import utilforplgs as ufp
import os
import re
import sys

import cv2


"""
ハッシュpHashでリネームする
"""
args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)

    hash_func = cv2.img_hash.PHash_create()
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                sample_image01 = ufp.my_imread(sep)
                tem = hash_func.compute(sample_image01)[0]
                a = "".join([hex(i)[2:] for i in tem])
                _, ext = os.path.splitext(sep)
                try:
                    os.rename(sep, a + ext)
                except (FileExistsError, PermissionError):
                    # 重複は保持しない
                    os.remove(sep)

                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
