# coding: utf-8

import virtualbox
import time

class VirtualBoxOperate:
    __vbox = virtualbox.VirtualBox()
    __session = virtualbox.Session
    __progress = None
    def __init__(self, name__or__id:str=None):
        self.__name = name__or__id

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
        self.__progress = self.__vm.launch_vm_process(session=self.__session, name='gui', environment='')
        time.sleep()