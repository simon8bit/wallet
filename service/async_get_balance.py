"""
-------------------------------------------------
   File Name:        sync_get_balance.py
   Description:      
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""

import requests
from PySide6.QtCore import QThread, Signal

from utils.tron_sdk_service import TronService


class AsyncRequestBalance(QThread):
    success = Signal(object)  # 成功回调（返回 json/text）
    error = Signal(str)  # 失败回调

    def __init__(self, address):
        super().__init__()
        self.address = address
        print("hello")

    def run(self):
        try:
            result = TronService.get_balance(address=self.address)
            self.success.emit(result)
            print(result)
        except Exception as e:
            self.error.emit(str(e))
