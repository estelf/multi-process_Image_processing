"""
クオリティの低いデータを計算し削除する拡張機能

"""
import utilforplgs as ufp
import os
import re
import sys

import cv2


args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]
model_path = "..\\brisque_model_live.yml"  # BRISQUEモデルデータ
range_path = "..\\brisque_range_live.yml"  # BRISQUE範囲データ


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
                score1 = cv2.quality.QualityBRISQUE_compute(img, model_path, range_path)

                # #print(score1[0])  #スコア表示させたいときだけ

                if score1[0] > 47:  # 数値を変えるだけ
                    os.remove(sep)

                # ###-------------------------------------### #

    os.chdir("..")


main(starts, step, flname)
