# coding: utf-8

from time import sleep
import requests
import json

#VirusTotalアクセスクラス
class VirusTotalOperate:
    __apikey:dict
    vturl = "https://www.virutotal.com/vtapi/v2/"
    apiurl = {"scan" :"file/scan",'rescan':'file/rescan',
              'report':'file/report', 'url_scan':'url/scan', 'url_report':'url/report'}
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
            return response.json()['resource']
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return None

    #ファイルの再キャン
    def fileReScan(self,filename:str, resource:str):
        try:
            params = {'apikey':self.__apikey["apikey"], 'resource':resource}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['rescan']), params=params)
            return response.json()['resource']
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return  None

    #レポートの取得
    def getReport(self,resource:str):
        try:
            params = {'apikey':self.__apikey["apikey"], 'resource':resource}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['report']), params=params)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return  None

    #URLスキャン
    def urlScan(self,url:str):
        try:
            params = {'apikey': self.__apikey["apikey"], 'url': url}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['url_scan']), params=params)
            return response.json()['url']
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return None

    #URLレポートの取得
    def getUrlReport(self,resource:str):
        try:
            params = {'apikey':self.__apikey["apikey"], 'resource':resource}
            response = requests.post("{}{}".format(self.vturl, self.apiurl['url_report']), params=params)
            return response.json()
        except Exception as e:
            print(response.status_code)
            self.__RateError()
            return  None

#Scan結果のJsonデータを操作
class VTReportOperate:
    report:dict
    name:str
    def __init__(self,name:str):
        self.name = name

    #スキャン結果
    def getResource(self, scandata)->str:
        return scandata['resource']

    #レポートをセット
    def setReport(self, repot:dict):
        self.report = repot
        return

    #陽性を示した数を返却
    def getPositives(self)->int:
        return self.report['positives']

