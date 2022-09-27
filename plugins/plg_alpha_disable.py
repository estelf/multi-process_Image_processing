
import cv2
import numpy as np
import glob
import os
import sys
import time
args=sys.argv

starts=int(args[3])
step=int(args[2])
flname=args[1]
"""
ファイル名を入力するとアルファチャンネルを削除し白で埋めた画像が表示されます。
"""



def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, -1)
        return img
    except Exception as e:
        print(e)
        return None
def my_imwrite(filename, img):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def main(starts,step,flname):
    os.chdir(flname)
    for i,sep in enumerate(glob.glob("*.png")):
        #print(i,sep)
        if (i-starts)%step==0:
            #print(i,starts,step)
            img=my_imread(sep)
            ####-------------------------------------####
            try:
                h, w, c = img.shape
                if c > 3:
                    flg = np.where(img[:, :, 3] < 10, True, False)
                    for i, sep in enumerate(flg):
                        for ii, sepii in enumerate(sep):
                            if sepii:
                                # print(img[i][ii])
                                img[i][ii] = [255, 255, 255, 255]

                    img = img[:, :, :3]
                    my_imwrite(sep,img)
            except Exception:
                pass
            ####-------------------------------------####


    os.chdir("..")
#start_time = time.perf_counter()
main(starts,step,flname)
#end_time = time.perf_counter()
 
# 経過時間を出力(秒)
#elapsed_time = end_time - start_time
#print(elapsed_time,"秒")
