import cv2
import numpy as np
import glob
import os
import sys
import time
import shutil
import dlib
from PIL import Image


args=sys.argv


starts=int(args[3])
step=int(args[2])
flname=args[1]


def detect_dlib(image):
    face_detector = dlib.simple_object_detector("../detector_face.svm")

    # 顔の検出
    faces = face_detector(image)
    a=[[(rect.left(), rect.top()), (rect.right(), rect.bottom())] for rect in faces]
    return a

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
    os.makedirs("OK",exist_ok=True)
    os.makedirs("NG",exist_ok=True)
    for i,sep in enumerate(glob.glob("*.png")):
        #print(i,sep)
        if (i-starts)%step==0:
            #print(i,starts,step)
            img=my_imread(sep)

            ####-------------------------------------####
            #print(sep)
   
            faces2=detect_dlib(img)
            if len(faces2)>0:
                shutil.move(sep,"OK")
            else:
                shutil.move(sep,"NG")
            ####-------------------------------------####


    os.chdir("..")
#start_time = time.perf_counter()
main(starts,step,flname)
#end_time = time.perf_counter()
 
# 経過時間を出力(秒)
#elapsed_time = end_time - start_time
#print(elapsed_time,"秒")