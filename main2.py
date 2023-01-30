"""
プログラム
マルチプロセス、プラグイン機能に対応した画像一括編集・動画切り出しプログラムです

"""
import argparse
import glob
import os
import subprocess
import time
import re
import cv2

# 顔切り抜き　シングル 452.9806762999997


class run_shell:

    """
    run(cmd_in: str) -> object   subprocessのrunと一緒
    Popen(cmd_in: str) -> object subprocessのPopenと一緒
    """

    def run(cmd_in: str) -> object:
        if os.name == "nt":
            out_out = subprocess.run(
                cmd_in,
                shell=True,
                encoding="utf-8",
                errors="ignore",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            out_out = subprocess.run(
                "exec " + cmd_in,
                shell=True,
                encoding="utf-8",
                errors="ignore",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return out_out

    def Popen(cmd_in: str) -> object:
        if os.name == "nt":
            out_out = subprocess.Popen(
                cmd_in,
                shell=True,
                encoding="utf-8",
                errors="ignore",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            out_out = subprocess.Popen(
                "exec " + cmd_in,
                shell=True,
                encoding="utf-8",
                errors="ignore",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return out_out


def get_flame_split(filename):
    """
    フレーム総数の出力
    """
    cap = cv2.VideoCapture(filename)
    max_flame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return int(max_flame_num)


def alive_check(polls, process_alive_list):
    """
    リストに入ったプロセス情報の実行状況を出力する
    """
    for iii, seps in enumerate(polls):
        if iii == 0:
            print("║", end="", flush=True)

        print(f"task{iii}", end="", flush=True)
        if seps is None:
            print(" \033[36m█\033[m║ ", end="", flush=True)
        else:
            if process_alive_list[iii].returncode != 0:
                print(" \033[31m█\033[m║ ", end="", flush=True)
            else:
                print(" \033[32m█\033[m║ ", end="", flush=True)
    else:
        print("", end="\r", flush=True)


def expmain(flname, extensions, process):
    """
    画像の加工プロセスを作成する部分。
    """

    print("プラグイン動作開始")
    print(f'python "{str(extensions)}" "{flname}" {process} {0}')

    process_alive_list = [
        run_shell.Popen(f'python "{str(extensions)}" "{flname}" {process} {i}') for i in range(process)
    ]

    polls = [i.poll() for i in process_alive_list]
    while None in polls:
        alive_check(polls, process_alive_list)

        polls = [i.poll() for i in process_alive_list]
    else:
        alive_check(polls, process_alive_list)


parser = argparse.ArgumentParser(description="マルチプロセス、プラグイン機能に対応した画像一括編集・動画切り出しプログラムです。")
parser.add_argument("folder", help="データのあるフォルダ名")  # 必須の引数を追加
parser.add_argument(
    "-ns", "--non_split", help="すでに切り分けられた画像ファイルを使用するフラグ", action="store_true"
)  # よく使う引数なら省略形があると使う時に便利
parser.add_argument("-p", "--process", help="プラグインのプロセス数 デフォルトは5", default=5, type=int)  # よく使う引数なら省略形があると使う時に便利
parser.add_argument("-e", "--extensions", help="使用したいプラグインのパス。カンマ区切りで複数指定可")  # よく使う引数なら省略形があると使う時に便利

args = parser.parse_args()

# print(args.non_split)
print("-------------------------")
if args.non_split is False:
    print("動画フォルダ名 : " + args.folder)
else:
    print("画像フォルダ名 : " + args.folder)
if args.extensions:
    print("プロセス数 : " + str(args.process))
    print("プラグインのパス : " + str(args.extensions))
print("-------------------------")


if args.non_split is False:
    for num, i in enumerate(glob.glob(args.folder + "//*")):
        if re.search(r".*\.mp4|mkv|ts|m2ts|webm$", str(i), re.I):
            start_time = time.perf_counter()  # 計測開始

            print(f"{i}を分離しています...")

            max_flame_num = get_flame_split(i)
            keta = len(str(max_flame_num))
            flname = os.path.splitext(i.split("\\")[-1])[0]
            os.makedirs(str(num), exist_ok=True)

            cmd = run_shell.run(f'ffmpeg -y -i "{i}" -vcodec png "{num}\\{flname[:15]}_%0{keta}d.png"')
            if cmd.returncode != 0:
                print(f"失敗しました\n{cmd}")
                continue
            else:

                print("成功しました")

            if args.extensions:
                for iii in str(args.extensions).split(","):
                    expmain(str(num), iii, args.process)

            end_time = time.perf_counter()
            # 経過時間を出力(秒)
            elapsed_time = end_time - start_time
            print("\n総処理時間", elapsed_time, "秒")
            print()
        else:
            print(f"未対応file{i}")
        # straw step
else:
    if args.extensions:
        start_time = time.perf_counter()  # 計測開始
        for iii in str(args.extensions).split(","):
            expmain(args.folder, iii, args.process)

        end_time = time.perf_counter()
        # 経過時間を出力(秒)
        elapsed_time = end_time - start_time
        print("\n総処理時間", elapsed_time, "秒")
        print()
