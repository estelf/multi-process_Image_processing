# --- クラスと関数の定義 ---
import numpy as np
import os
import time
import PIL.Image
import scipy.ndimage
import dlib
import sys
import pprint
import cv2
import glob

# --------- ランドマーク検出 -------------
class LandmarksDetector:
    def __init__(self, predictor_model_path):
        """
        :param predictor_model_path: path to shape_predictor_68_face_landmarks.dat file
        """
        self.detector = dlib.get_frontal_face_detector(
        )  # cnn_face_detection_model_v1 also can be used
        self.shape_predictor = dlib.shape_predictor(predictor_model_path)

    def get_landmarks(self, image):

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = self.detector(img, 1)

        for detection in dets:
            face_landmarks = [(item.x, item.y)
                              for item in self.shape_predictor(img, detection).parts()]
            yield face_landmarks
#---------画像表示PIL-------------
def show(img):
    img= np.array(img, dtype=np.uint8)
    cv2.imshow("test",img[:,:,::-1])
    cv2.waitKey()
# ---------- データを増やす --------------
def mizumasi():
    os.chdir("train")
    for i in glob.glob("*.png"):
        img=cv2.imread(i)
        #print(i,img)
        img=cv2.flip(img,1)
        
        cv2.imwrite("flip_"+i,img)
    os.chdir("..")
# ---------- 顔画像の切り出し --------------
def image_align(src_file, dst_file, face_landmarks, output_size=1024, transform_size=4096, enable_padding=True):
    # Align function from FFHQ dataset pre-processing step
    # https://github.com/NVlabs/ffhq-dataset/blob/master/download_ffhq.py
    lm = np.array(face_landmarks)
    lm_chin = lm[0: 17]  # left-right
    lm_eyebrow_left = lm[17: 22]  # left-right
    lm_eyebrow_right = lm[22: 27]  # left-right
    lm_nose = lm[27: 31]  # top-down
    lm_nostrils = lm[31: 36]  # top-down
    lm_eye_left = lm[36: 42]  # left-clockwise
    lm_eye_right = lm[42: 48]  # left-clockwise
    lm_mouth_outer = lm[48: 60]  # left-clockwise
    lm_mouth_inner = lm[60: 68]  # left-clockwise

    # Calculate auxiliary vectors.
    eye_left = np.mean(lm_eye_left, axis=0)
    eye_right = np.mean(lm_eye_right, axis=0)
    eye_avg = (eye_left + eye_right) * 0.5
    eye_to_eye = eye_right - eye_left
    mouth_left = lm_mouth_outer[0]
    mouth_right = lm_mouth_outer[6]
    mouth_avg = (mouth_left + mouth_right) * 0.5
    eye_to_mouth = mouth_avg - eye_avg

    # Choose oriented crop rectangle.
    x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
    x /= np.hypot(*x)
    x *= max(np.hypot(*eye_to_eye) * 2.0, np.hypot(*eye_to_mouth) * 1.8)
    y = np.flipud(x) * [-1, 1]
    c = eye_avg + eye_to_mouth * 0.1
    quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
    qsize = np.hypot(*x) * 2


    img = src_file

    # Shrink.
    shrink = int(np.floor(qsize / output_size * 0.5))
    if shrink > 1:
        rsize = (int(np.rint(float(img.size[0]) / shrink)),
                 int(np.rint(float(img.size[1]) / shrink)))
        img = img.resize(rsize, PIL.Image.ANTIALIAS)
        quad /= shrink
        qsize /= shrink

    # Crop.
    border = max(int(np.rint(qsize * 0.1)), 3)
    crop = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(
        np.ceil(max(quad[:, 0]))), int(np.ceil(max(quad[:, 1]))))
    crop = (max(crop[0] - border, 0), max(crop[1] - border, 0),
            min(crop[2] + border, img.size[0]), min(crop[3] + border, img.size[1]))
    if crop[2] - crop[0] < img.size[0] or crop[3] - crop[1] < img.size[1]:
        img = img.crop(crop)
        quad -= crop[0:2]

    # Pad.
    pad = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(
        np.ceil(max(quad[:, 0]))), int(np.ceil(max(quad[:, 1]))))
    pad = (max(-pad[0] + border, 0), max(-pad[1] + border, 0), max(pad[2] -
                                                                   img.size[0] + border, 0), max(pad[3] - img.size[1] + border, 0))
    if enable_padding and max(pad) > border - 4:
        #show(img)
        pad = np.maximum(pad, int(np.rint(qsize * 0.3)))
        img=np.float32(img)
        #pprint.pprint(aabb)
        #print()
        #[round(np.mean(aabb[:,0])),round(np.mean(aabb[:,1])),round(np.mean(aabb[:,2]))]
        #pprint.pprint(img)
        img = np.pad(img,
                     ((pad[1], pad[3]), (pad[0], pad[2]), (0, 0)), "constant",
                     constant_values=((
                         [round(np.mean(img[0,:,0])),round(np.mean(img[0,:,1])),round(np.mean(img[0,:,2]))], 
                     [round(np.mean(img[-1,:,0])),round(np.mean(img[-1,:,1])),round(np.mean(img[-1,:,2]))]), 
                     ([round(np.mean(img[:,0,0])),round(np.mean(img[:,0,1])),round(np.mean(img[:,0,2]))],
                      [round(np.mean(img[:,-1,0])),round(np.mean(img[:,-1,1])),round(np.mean(img[:,-1,2]))]), (0, 0)))
        #show(img)
        h, w, _ = img.shape
        y, x, _ = np.ogrid[:h, :w, :1]
        mask = np.maximum(1.0 - np.minimum(np.float32(x) / pad[0], np.float32(
            w-1-x) / pad[2]), 1.0 - np.minimum(np.float32(y) / pad[1], np.float32(h-1-y) / pad[3]))
        blur = qsize * 0.02
        img += (scipy.ndimage.gaussian_filter(img,
                                              [blur, blur, 0]) - img) * np.clip(mask * 3.0 + 1.0, 0.0, 1.0)
        #show(img)
        img += (np.median(img, axis=(0, 1)) - img) * np.clip(mask, 0.0, 1.0)
        #show(img)
        img = np.uint8(np.clip(np.rint(img), 0, 255))
        #show(img)
        quad += pad[:2]
        """
        #適応的ヒストグラム平坦化
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # hsv票色系に変換
        h,s,v = cv2.split(hsv) # 各成分に分割
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3, 3))
        result = clahe.apply(v)
        hsv = cv2.merge((h,s,result))
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        """
        #PIL
        img=PIL.Image.fromarray(img, 'RGB')


    # Transform.
    img = img.transform((transform_size, transform_size),
                        PIL.Image.QUAD, (quad + 0.5).flatten(), PIL.Image.BILINEAR)
    if output_size < transform_size:
        img = img.resize((output_size, output_size), PIL.Image.ANTIALIAS)

    # Save aligned image.
    img.save(dst_file, 'PNG')



def main(landmarks_model_path="..\\shape_predictor_68_face_landmarks.dat",output_size=256,starts=0,step=0):

    # 顔画像の切り出し
    landmarks_detector = LandmarksDetector(landmarks_model_path)

    dirlist_my=glob.glob("*.*")
    for ii,img_name in enumerate(dirlist_my):
        if re.search(r".*\.j?pe?n?g$",str(i),re.I):
            try:
                if (ii-starts)%step==0:
                    print(img_name,flush=True)

                    img=cv2.imread(img_name)

                    for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(img), start=1):
                        face_img_name = f'{os.path.splitext(img_name)[0]}_trm_{i}.png'

                        aligned_face_path = face_img_name
                                    
                        
                        #print("st")
                        image_align(PIL.Image.fromarray(img[:,:,::-1]), aligned_face_path, face_landmarks,output_size=output_size, transform_size=1024)
                        #print("ed")
                    else:
                        os.remove(img_name)
            except Exception:
                continue
            
    print("FINISH!!!",flush=True)

args=sys.argv
starts=int(args[3])
step=int(args[2])
flname=args[1]
os.chdir(flname)
main(starts=int(args[3]),step=int(args[2]))
os.chdir("..")


