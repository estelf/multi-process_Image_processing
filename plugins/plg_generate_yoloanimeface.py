import utilforplgs as ufp
import os
import re
import sys

import cv2
import dlib

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


# 顔検出器
face_detector = dlib.simple_object_detector("./detector_face.svm")


def detect(img_path):
    base = os.path.basename(img_path)[:-4]
    # 画像ファイルを開く
    image = ufp.my_imread(img_path)

    h, w, _ = image.shape
    # 顔の検出
    faces = face_detector(image)
    rakulist = []
    if len(faces) == 0:
        return 0
    elif len(faces) > 0:
        for rect in faces:
            # 座標取得
            x_start = rect.left()
            x_end = rect.right()
            y_start = rect.top()
            y_end = rect.bottom()
            # サイズ取得
            face_width = x_end - x_start
            face_height = y_end - y_start
            # 長方形の場合、弾く
            if abs(face_width - face_height) > 3:
                continue
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 255), thickness=2)
            rakulist.append(
                f"{0} {(x_end + x_start) / (2 * w)} {(y_end + y_start) / (2 * h)} {(x_end - x_start) / w} {(y_end - y_start) / h}"
            )
    # 顔部分を赤線で囲った画像の保存
    # cv2.imshow("aa", imutils.resize(image, width=512))
    # aaa = cv2.waitKey()
    # if aaa == 32:
    # print("save")
    with open(f"labels\\{base}.txt", "w") as f:
        f.write("\n".join(rakulist))

    # #print(f"{0} {(x2 + x1) / (2 * w)} {(y2 + y1) / (2 * h)} {(x2 - x1) / w} {(y2 - y1) / h}")
    # cv2.imwrite(img_path, image)


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                # #print(i,starts,step)

                # ###-------------------------------------####

                detect(sep)

                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
