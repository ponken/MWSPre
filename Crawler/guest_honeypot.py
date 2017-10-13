# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import subprocess
from smb.SMBConnection import SMBConnection
from datetime import datetime as dt

#sys.path.append("Z:\\")
import guest_crawler
import guest_binmatch

# クローラスレッドのみTrueにできる
heartbeat = False
heartbeat_lock = threading.Lock()

# クローラスレッドからのメインスレッドへの終了命令フラグ
processend = False
processend_lock = threading.Lock()

raw_url = ""
pagenum = 0
prevurl = ""

class Crawler(threading.Thread):
    #マルチスレッド起動
    def __init__(self, restore=False):
        threading.Thread.__init__(self)
        self.restore = restore

    def run(self):
        global heartbeat
        global heartbeat_lock
        global processend
        global processend_lock
        global raw_url
        global pagenum
        global prevurl

        #google検索結果のクローラ
        crawler = guest_crawler.GoogleWebCrawler()

        #中断された場所から
        if self.restore == True:
            crawler.restore(raw_url, pagenum)
            links = crawler.get_links()
            for i in range(len(links)):
                if links[i] == prevurl:
                    print("find previous link\n >", prevurl)
                    del links[:i+1]
                    break
        #初回起動時
        else:
            conn = SMBConnection("", "", "", "", domain="", use_ntlm_v2=True)
            conn.connect("192.168.2.111", 445)

            #NAS上の検索ワードをローカルに移動
            with open("setfile_searchword.txt", "wb") as file_obj:
                conn.retrieveFile("share", "\\setfile_searchword.txt", file_obj)

            conn.close()

            #検索ワードの指定
            with open("setfile_searchword.txt", "rb") as fin:
                search_word = fin.read()
                search_word = search_word.decode("utf-8")

            os.remove("setfile_searchword.txt")

            #検索ワードをクローラに渡す
            crawler.search(search_word)
            links = crawler.get_links()

        while True:
            #1ページの全検索結果をクロール
            for link in links:
                #クローラ生存確認
                if heartbeat_lock.acquire() == True:
                    print("heartbeat sent")
                    heartbeat = True
                    heartbeat_lock.release()
                raw_url = crawler.get_raw_url()
                pagenum = crawler.get_current_pagenum()
                prevurl = link
                print(pagenum, link)
                crawler.open_links([link])

            #次の検索結果ページに
            crawler.goto_next_page()

            #現在の検索結果ページが50を超えたら終了
            if crawler.get_current_pagenum() >= 50:
                if processend_lock.acquire() == True:
                    processend = True
                    print("thread end")
                    processend_lock.release()
                    break
            else:
                links = crawler.get_links()

            time.sleep(1.0)

#このpythonスクリプトはWindowsによって自動的に起動される
if __name__ == '__main__':
    # tshark起動
    tshark = subprocess.Popen("tshark -i 1 -w test.pcapng")
    time.sleep(4.0)

    # マルチスレッドでクローラを起動
    crawler = Crawler()
    crawler.start()

    start = time.time()

    while True:
        #少し待機
        time.sleep(0.5)

        #クローラが異常終了していないか確認
        if heartbeat_lock.acquire() == True:
            if heartbeat == True:
                print("heartbeat received")
                start = time.time()
                heartbeat = False
            heartbeat_lock.release()

        #クローラがフリーズしてそうだったらクローラを再起動
        interval = int(time.time() - start)
        print(interval)
        if interval > 20:
            os.system("""taskkill /im "iexplore.exe" /f""")
            crawler = Crawler(True)
            crawler.start()
            time.sleep(10.0)
            start = time.time()

        #クローラから終了命令が出ていれば終了
        if processend_lock.acquire() == True:
            if processend == True:
                print("process end")
                break
            processend_lock.release()

    # tshark終了と終了待機
    tshark.terminate()
    tshark.wait()

    # 少し待機
    time.sleep(4.0)

    # pcapngをpcapに変換
    os.system("editcap -F libpcap -T ether test.pcapng test.pcap")

    # パケット中にexeファイルが現れたらNASにpcapを転送
    if guest_binmatch.pcap_traffick_matching("test.pcap"):
        conn = SMBConnection("", "", "", "", domain="", use_ntlm_v2=True)
        conn.connect("192.168.2.111", 445)

        storefile = "test_" + dt.now().strftime('%Y/%m/%d') + ".pcap"
        with open("test.pcap", "rb") as file_obj:
            conn.storeFile("share", "\\" + storefile, file_obj)

        conn.close()
        os.remove("test.pcap")

    #Windowsを終了させる。ホスト側が自動的に再起動させる
    os.system("shutdown -s -f")
