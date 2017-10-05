# -*- coding: utf-8 -*-

import sys
import dpkt
import socket

def pcap_traffick_matching(filename):
    patternlist = [
        "This program must be run under Win32",
        "This program cannot be run in DOS mode",
        "This program",
        "be run",
        "under Win32",
        "DOS mode"
    ]

    patternlist = [pattern.encode("utf-8") for pattern in patternlist]

    with open("test.pcap", "rb") as f:
        line = 0

        for ts, buf in dpkt.pcap.Reader(f):
            line += 1

            try:
                eth = dpkt.ethernet.Ethernet(buf)
            except:
                continue

            if type(eth.data) == dpkt.ip.IP:
                ip = eth.data

                if type(ip.data) == dpkt.tcp.TCP:
                    tcp = ip.data

                    if (True in [bool(tcp.data.find(pattern)+1) for pattern in patternlist]) == True:
                        print("line", line)
                        print(tcp.data)
                        break
