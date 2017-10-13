# -*- coding: utf-8 -*-

import os
import csv
import sys
import time
import argparse
import subprocess
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":
    #検索ワードリストの何行目から始めるか指定可能
    args = argparse.ArgumentParser()
    args.add_argument("-i", required=True, type=int, help="start ID")
    args = args.parse_args()
    word_ID = args.i

    vmname = "IE8 - Win7"
    ssname = "SS0605"
    print("VM名 : " + vmname + " (スクリーンショット : " + ssname + ")")

    while True:
        # 検索ワードの準備
        word_list = [word[0] for word in csv.reader(open("wordlist.csv", "r"))]

        if word_ID < len(word_list):
            search_word = word_list[word_ID]
        else:
            sys.exit()

        print("\n検索ワード ID " + str(word_ID) + " : " + search_word)

        # NASへの検索ワードの転送
        conn = SMBConnection("", "", "", "", domain="", use_ntlm_v2=True)
        conn.connect("192.168.2.111", 445)

        with open("setfile_searchword.txt", "w") as fout:
            fout.write(search_word)

        with open("setfile_searchword.txt", "rb") as file_obj:
            conn.storeFile("share", "\\setfile_searchword.txt", file_obj)

        os.remove("setfile_searchword.txt")

        conn.close()

        # VM起動
        print("\nVMを起動中...")
        vmproc = subprocess.Popen("""VBoxManage startvm \"""" + vmname + """\"""", shell=True)
        vmproc.wait()

        # VMが生きてるか確認
        while True:
            time.sleep(5.0)
            print("\nVMの存在を確認中...")
            result = subprocess.check_output("VBoxManage list runningvms".split(" "))
            if len(result) == 0:
                print("VMの存在を確認できません")
                break
            else:
                print("VMの存在を確認")

        # SSリストア
        time.sleep(5.0)
        print("\nスナップショットをリストア中...")
        vmproc = subprocess.Popen("""VBoxManage snapshot \"""" + vmname + """\" restore \"""" + ssname + """\"""", shell=True)
        vmproc.wait()

        # 次の検索ワードを指定
        time.sleep(10.0)
        print("\n次のワードを検索...")
        word_ID += 1
