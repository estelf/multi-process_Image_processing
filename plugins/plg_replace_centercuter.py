import utilforplgs as ufp
import os
import re
import sys

from PIL import Image


args = sys.argv

"""
画像が正方形になるように両側もしくは上下から切り取る
"""
starts = int(args[3])
step = int(args[2])
flname = args[1]


def crop_center(img, crop_width, crop_height):
    img_width, img_height = img.size
    return img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)

    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = Image.open(sep)

                # ###-------------------------------------####
                img_crop_square = crop_center(img, min(img.size), min(img.size))
                img_crop_square.save(sep)
                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
