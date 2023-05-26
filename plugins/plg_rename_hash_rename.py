import utilforplgs as ufp
import hashlib
import os
import re
import sys


"""
ハッシュmd5名でリネームする
"""
args = sys.argv


starts = int(args[3])
step = int(args[2])
flname = args[1]


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


@ufp.Trace2file(starts)
def main(starts, step, flname):
    aldf = ufp.filereader()
    os.chdir(flname)
    for i, sep in enumerate(aldf):
        if re.search(r".*\.j?pe?n?g$", str(sep), re.I):
            # #print(i,sep)
            if (i - starts) % step == 0:
                a = has(sep)
                _, ext = os.path.splitext(sep)
                try:
                    os.rename(sep, a + ext)
                except (FileExistsError, PermissionError):
                    os.remove(sep)

                # ###-------------------------------------####

    os.chdir("..")


main(starts, step, flname)
