# coding: utf-8

import virtualbox
import time
from msvcrt import getch

class VirtualBoxOperate:
    __vbox = virtualbox.VirtualBox()
    __session = virtualbox.Session()
    # __console
    __progress = None
    def __init__(self, name__or__id:str, snapshot_name_or_id:str):
        self.__name = name__or__id
        self.__snapshot = snapshot_name_or_id

    # name__or__idと一致するVMがあることを確認
    def checkNameId(self)->bool:
        try:
            self.__vm = self.__vbox.find_machine(self.__name)
            return True
        except:
            print('\"{}\" is None.'.format(self.__name))
            return False

    #VM起動
    def startVM(self):
        self.__progress = self.__vm.launch_vm_process(self.__session, 'gui', '')
        self.__console = self.__vm.create_session()
        time.sleep(20)

    #入力した文字をVMに入力(EOFが来たら終了)
    def inputKeyboard(self):
        # print()
        # input_key=''
        while(True):
            try:
                input_key = input('Input or EOF>:')
                # print(input_key)
                # Nがnに変換される（なぞ）、日本語は遅れない
                self.__session.console.keyboard.put_keys(input_key+'\n')
            except EOFError:
                break

    #キー情報を送る(未完)
    def inputKey(self):
        while (True):
            try:
                print('press:')
                press_key = ord(getch())
                print('hold :')
                hold_key = ord(getch())
                self.__session.console.keyboard.put_keys(press_keys=hex(91), hold_keys=None)
            except EOFError:
                break

    # ログイン（Win ver）(未テスト)
    def loginWindows(self):
        username = input('username>:')
        passwd   = input('password>:')
        with self.__vm.create_session() as session:
            with session.console.guest.create_session(user=username,password=passwd) as gs:
                print(gs.directory_exists("C:\\Windows"))

    #スナップショットの確認
    def checkSnapshot(self)->bool:
        try:
            self.__vmsnap = self.__vm.find_snapshot(self.__snapshot)
            return True
        except:
            print('\"{}\" is None.'.format(self.__snapshot))
            return False

    #VM終了
    def endVM(self):
        self.__session.console.power_down()
        time.sleep(10)
        if self.checkSnapshot():
            self.__vm.restore_snapshot(self.__vmsnap)

    def test(self):
        # while (True):
        #     try:
        #         a = input('num:')
        #         a = int(a)
        #         self.__session.console.keyboard.put_keys(press_keys=['LWIN'], hold_keys=None)
        #     except EOFError:
        #         break
        input('test:')
        gs = self.__vm.create_session().console.guest.create_session(user='test',password='testpass')
        print(gs)
        print(self.__session.state)
        gs.execute(command="C:\\Windows\\System32\\cmd.exe")

        # # try:
        # print(gs.directory_exists(path='C:\\Windows\\'))
        # except :
        #     print('error')
