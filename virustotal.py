# coding: utf-8

from time import sleep
import requests
import json

class VirusTotalOperate():
    __apikey:dict
    vturl = "https://www.virutotal.com/vtapi/v2/"
    apiurl = {"scan" :"file/scan",'rescan':'file/rescan',
              'report':'file/report', 'url_scan':'url/scan'}
    def __init__(self, apikey:str):
        self.__apikey = {"apikey":apikey}

    #レートエラー
    def __RateError(self):
        sleep(60)
        return

    #ファイルの送信
    def fileScan(self, filename:str):
        try:
            files = {'file':(filename, open(filename,'rb'))}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['scan']), files=files, params=self.__apikey)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return False

    #ファイルの再キャン
    def fileReScan(self,filename:str, resource:str):
        try:
            params = {'apikey':self.__apikey["apikey"], 'resource':resource}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['rescan']), params=params)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return  False

    #レポートの取得
    def getReportJson(self,resource:str):
        try:
            params = {'apikey':self.__apikey["apikey"], 'resource':resource}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['report']), params=params)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return  False

    #URLスキャン
    def urlScan(self,url:str):
        try:
            params = {'apikey': self.__apikey["apikey"], 'url': url}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['url_scan']), params=params)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return False
