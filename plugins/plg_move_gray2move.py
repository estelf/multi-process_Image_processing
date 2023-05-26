import utilforplgs as ufp
import os
import re
import shutil
import sys

from PIL import Image, ImageStat

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    pil_img = file
    bands = pil_img.getbands()
    if bands == ("R", "G", "B") or bands == ("R", "G", "B", "A"):
        thumb = pil_img.resize((thumb_size, thumb_size))
        SSE, bias = 0, [0, 0, 0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias) / 3 for b in bias]
        for pixel in thumb.getdata():
            mu = sum(pixel) / 3
            SSE += sum((pixel[i] - mu - bias[i]) * (pixel[i] - mu - bias[i]) for i in [0, 1, 2])
        MSE = float(SSE) / (thumb_size * thumb_size)
        if MSE <= MSE_cutoff:
            return "g"
        else:
            return "c"


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    os.makedirs("ggg", exist_ok=True)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)
                img = Image.open(sep)

                # ###-------------------------------------### #
                if detect_color_image(img) == "g":
                    shutil.move(sep, "ggg")

                # ###-------------------------------------### #

    os.chdir("..")


# sta
main(starts, step, flname)
