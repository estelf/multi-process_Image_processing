import cv2
import numpy as np
import glob
import os
import sys
from PIL import Image
args=sys.argv


starts=int(args[3])
step=int(args[2])
flname=args[1]
def crop_center(img, crop_width, crop_height):
    img_width, img_height = img.size
    return img.crop(((img_width - crop_width) // 2,(img_height - crop_height) // 2,(img_width + crop_width) // 2,(img_height + crop_height) // 2))
def main(starts,step,flname):
    os.chdir(flname)
    for i,sep in enumerate(glob.glob("*.png")):
        #print(i,sep)
        if (i-starts)%step==0:
            #print(i,starts,step)
            img = Image.open(sep)

            ####-------------------------------------####
            img_crop_square = crop_center(img, min(img.size), min(img.size))
            img_crop_square.save(sep)
            ####-------------------------------------####


    os.chdir("..")
#start_time = time.perf_counter()
main(starts,step,flname)
#end_time = time.perf_counter()
 
# 経過時間を出力(秒)
#elapsed_time = end_time - start_time
#print(elapsed_time,"秒")