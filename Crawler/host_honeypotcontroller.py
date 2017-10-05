# -*- coding: utf-8 -*-

import os
import csv
import sys
import time
import argparse
import subprocess
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-i", required=True, type=int, help="start ID")
    args = args.parse_args()
    word_ID = args.i

    vmname = "IE8 - Win7"
    ssname = ""
    print("VM name : " + vmname + " (ssname : " + ssname + ")")

    while True:
        # 検索ワードの準備
        word_list = [word[0] for word in csv.reader(open("wordlist.csv", "r"))]

        if word_ID < len(word_list):
            search_word = word_list[word_ID]
        else:
            sys.exit()

        print("word ID " + str(word_ID) + " : " + search_word)

        # sambaへの一時ファイルの転送
        conn = SMBConnection("", "", "", "", domain="", use_ntlm_v2=True)
        conn.connect("192.168.10.100", 445)

        with open("set_searchword.txt", "w") as fout:
            fout.write(search_word)

        with open("set_searchword.txt", "rb") as file_obj:
            conn.storeFile("homeNAS", "\\HDPC-UT2\\set_searchword.txt", file_obj)

        os.remove("set_searchword.txt")

        conn.close()

        # VM起動
#        vmproc = subprocess.Popen("""VBoxManage startvm \"""" + vmname + """\"""", shell=True)
#        vmproc.wait()

        # VM死活確認
        while True:
            time.sleep(1.0)
            result = subprocess.check_output("VBoxManage list runningvms".split(" "))
            if len(result) == 0:
                break

        # SSリストア
#        vmproc = subprocess.Popen("""VBoxManage snapshot \"""" + vmname + """\" restore \"""" + ssname + """\"""", shell=True)
#        vmproc.wait()

        # 次の検索ワードを指定
        word_ID += 1
