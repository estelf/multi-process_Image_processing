import glob
import hashlib
import os
import re
import sys

import cv2
import numpy as np


args=sys.argv


starts=int(args[3])
step=int(args[2])
flname=args[1]
def has(x):
    algo = "md5"
    h = hashlib.new(algo)
    Length = hashlib.new(algo).block_size * 0x800
    path = x
    with open(path, "rb") as f:
        BinaryData = f.read(Length)
        while BinaryData:
            h.update(BinaryData)
            BinaryData = f.read(Length)
    return h.hexdigest()
def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(e)
        return None
def main(starts,step,flname):
    os.chdir(flname)
    for i,sep in enumerate(glob.glob("*.*")):
        if re.search(r".*\.j?pe?n?g$", str(i), re.I):
            #print(i,sep)
            if (i-starts)%step==0:
                a = has(sep)
                _, ext = os.path.splitext(sep)
                if os.path.exists(a+ext):
                    os.remove(sep)
                else:
                    os.rename(sep, a+ext)

                ####-------------------------------------####


    os.chdir("..")
#start_time = time.perf_counter()
main(starts,step,flname)
#end_time = time.perf_counter()
 
# 経過時間を出力(秒)
#elapsed_time = end_time - start_time
#print(elapsed_time,"秒")