import utilforplgs as ufp
import os
import sys

import numpy as np

args = sys.argv

starts = int(args[3])
step = int(args[2])
flname = args[1]
"""
ファイル名を入力するとアルファチャンネルを削除し白で埋めた画像が表示されます。
"""


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)

    for i, sep in enumerate(aldf):
        if (i - starts) % step == 0:
            img = ufp.my_imread(sep)
            # ###-------------------------------------####
            h, w, c = img.shape
            if c > 3:
                flg = np.where(img[:, :, 3] < 10, True, False)
                for i, sep2 in enumerate(flg):
                    for ii, sepii in enumerate(sep2):
                        if sepii:
                            img[i][ii] = [255, 255, 255, 255]

                img = img[:, :, :3]
                ufp.my_imwrite(sep, img)

            # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
