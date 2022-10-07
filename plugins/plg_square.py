import glob
import os
import sys
import re
import cv2
import numpy as np
import time

args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


def ryousika(img):
    Z = img.reshape((-1, 3))
    # np.float32型に変換
    Z = np.float32(Z)

    # k-meansの終了条件
    # デフォルト値を使用
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # 分割後のグループの数
    K = 8
    # k-means処理
    _, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # np.uint8型に変換
    center = np.uint8(center)
    # グループごとにグループ内平均値を割り当て
    res = center[label.flatten()]
    return res


def cal_border(arr):
    arr = ryousika(arr)
    unique0, freq0 = np.unique(arr, return_counts=True, axis=0)
    # print("a")
    # print(unique0, freq0)
    mode0 = unique0[np.argmax(freq0)]
    return (np.array(mode0)).astype(np.uint8)


def edge_blur(mask: np.array, padding_img: np.array, paddata):
    # マスクはブレンド率のこと！！！！！！！
    padding_img = np.copy(padding_img).astype(np.float32)
    two_clored_img = np.zeros_like(padding_img).astype(np.float32)

    t_h, t_w, _ = two_clored_img.shape

    for i, sep in enumerate(paddata):
        if sep:
            if i == 0:
                two_clored_img[: t_h // 2] = sep
            elif i == 1:
                two_clored_img[t_h // 2 :] = sep
            elif i == 2:
                two_clored_img[:, : t_w // 2] = sep
            elif i == 3:
                two_clored_img[:, t_w // 2 :] = sep

    kernel = np.ones((27, 27), np.uint8)
    # エロージョンで白部分を減らす
    mask = cv2.erode(np.copy(mask), kernel, iterations=1).astype(np.float32)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.blur(mask, (9, 9), 3)
    tem_img_1 = np.copy(padding_img).astype(np.float32)
    return (two_clored_img + (tem_img_1 - two_clored_img) * (mask / 255)).astype(np.uint8)


def resize_img(img):
    """
    画像をpaddingし

    """

    height, width, _ = img.shape  # 画像の縦横サイズを取得

    diffsize = abs(height - width)
    padding_half = int(diffsize / 2)
    # マスク用に画像本体部分が255になるようなデータ生成
    mask = np.copy(img)
    mask[:] = 255
    # print(mask.shape)

    # 縦長画像→幅を拡張する
    if height > width:

        left = cal_border(img[:, :16])
        right = cal_border(img[:, -16:])
        print("b", left, right)

        padding_img = cv2.copyMakeBorder(
            img, 0, 0, 0, height - (width + padding_half), cv2.BORDER_CONSTANT, value=right.tolist()
        )
        padding_img = cv2.copyMakeBorder(padding_img, 0, 0, padding_half, 0, cv2.BORDER_CONSTANT, value=left.tolist())

        # マスク

        mask = cv2.copyMakeBorder(
            mask, 0, 0, padding_half, height - (width + padding_half), cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )

        padding_img = edge_blur(mask, padding_img, (0, 0, left.tolist(), right.tolist()))

    # 横長画像→高さを拡張する
    elif width > height:
        top = cal_border(img[:16])
        bottom = cal_border(img[-16:])

        print("b", top, bottom)
        padding_img = cv2.copyMakeBorder(
            img, 0, width - (height + padding_half), 0, 0, cv2.BORDER_CONSTANT, value=bottom.tolist()
        )
        padding_img = cv2.copyMakeBorder(padding_img, padding_half, 0, 0, 0, cv2.BORDER_CONSTANT, value=top.tolist())

        mask = cv2.copyMakeBorder(
            mask, padding_half, width - (height + padding_half), 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )

        padding_img = edge_blur(mask, padding_img, (top.tolist(), bottom.tolist(), 0, 0))

    else:
        padding_img = img

    return padding_img


def my_imread(filename):
    try:
        n = np.fromfile(filename, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)

        if len(list(img.shape)) != 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img
    except Exception as e:
        print(e)
        return None


def my_imwrite(filename, img):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img)
        if result:
            with open(filename, mode="w+b") as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


"""img = my_imread("000a4d5c2956a7c1058eaab08a547558.png")
img = resize_img(img)
cv2.imshow("a", img)
cv2.waitKey()
my_imwrite("test.png", img)"""


def main(starts, step, flname):
    os.chdir(flname)
    aldf = glob.glob("*.*")
    time.sleep(1)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # print(i,sep)
            if (i - starts) % step == 0:
                # print(i,starts,step)
                img = my_imread(sep)

                # ###-------------------------------------### #
                img = resize_img(img)
                my_imwrite(sep, img)
                # ###-------------------------------------### #

    os.chdir("..")


# start_time = time.perf_counter()
main(starts, step, flname)
