# -*- coding: utf-8 -*-

import os
import sys
import threading
import time

sys.path.append("C:\\Users\\takayuki\\Desktop")
from Crawler import honeypot_crawler

heartbeat = False
heartbeat_lock = threading.Lock()

processend = False
processend_lock = threading.Lock()

raw_url = ""
pagenum = 0
prevurl = ""

class Crawler(threading.Thread):
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

        crawler = honeypot_crawler.GoogleWebCrawler()

        if self.restore == True:
            crawler.restore(raw_url, pagenum)
            links = crawler.get_links()
            for i in range(len(links)):
                if links[i] == prevurl:
                    print("find previous link\n >", prevurl)
                    del links[:i+1]
                    break
        else:
            crawler.search("ニコニコ動画")
            links = crawler.get_links()

        while True:
            for link in links:
                if heartbeat_lock.acquire() == True:
                    print("heartbeat sent")
                    heartbeat = True
                    heartbeat_lock.release()
                raw_url = crawler.get_raw_url()
                pagenum = crawler.get_current_pagenum()
                prevurl = link
                print(pagenum, link)
                crawler.open_links([link])

            crawler.goto_next_page()

            if crawler.get_current_pagenum() >= 1:
                if processend_lock.acquire() == True:
                    processend = True
                    print("thread end")
                    processend_lock.release()
                    break
            else:
                links = crawler.get_links()

            time.sleep(1.0)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.start()

    start = time.time()

    while True:
        time.sleep(0.5)

        if heartbeat_lock.acquire() == True:
            if heartbeat == True:
                print("heartbeat received")
                start = time.time()
                heartbeat = False
            heartbeat_lock.release()

        interval = int(time.time() - start)
        print(interval)
        if interval > 20:
            os.system("""taskkill /im "firefox.exe" /f""")
            crawler = Crawler(True)
            crawler.start()
            time.sleep(10.0)
            start = time.time()

        if processend_lock.acquire() == True:
            if processend == True:
                print("process end")
                break
            processend_lock.release()

    os.system("shutdown -s -f")
