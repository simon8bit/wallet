import sys
from functools import partial

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication, QWidget,
    QTableWidgetItem, QAbstractItemView,
    QHeaderView, QVBoxLayout, QSizePolicy, QCompleter, QHBoxLayout
)
from qfluentwidgets import TableWidget, PrimaryPushButton, SearchLineEdit, PrimaryToolButton, VBoxLayout
from qfluentwidgets import FluentIcon as FIF

from service.db_server import DBService
from utils.tron_sdk_service import TronService


# class MainWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._border_visible = False
#         self._border_radius = 0
#         self._update_style()
#
#     def setBorderVisible(self, visible: bool):
#         self._border_visible = visible
#         self._update_style()
#
#     def setBorderRadius(self, radius: int):
#         self._border_radius = radius
#         self._update_style()
#
#     def _update_style(self):
#         style = ""
#         if self._border_visible:
#             style += f"border: 1px solid #333;"
#         if self._border_radius > 0:
#             style += f"border-radius: {self._border_radius}px;"
#         self.setStyleSheet(style)


class MainWidget(QWidget):
    """最简版表格测试"""
    logoutRequested = Signal()

    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("表格展开测试")
        self.resize(600, 300)
        self.data = [
            {"address": "Txxxxxxx1", "created_at": "2026-02-08 10:00"},
            {"address": "Txxxxxxx2", "created_at": "2026-02-08 11:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
            {"address": "Txxxxxxx3", "created_at": "2026-02-08 12:00"},
        ]
        self.layout = QVBoxLayout(self)
        self.table = TableWidget()
        self.layout.addWidget(self.table)

        # 创建钱包按钮
        self.addBtn = PrimaryPushButton()
        self.addBtn.setText("创建钱包")
        self.addBtn.setIcon(FIF.ADD)
        self.addBtn.clicked.connect(self.createWallet)

        # 搜索框
        self.searchEdit = SearchLineEdit()
        self.searchEdit.searchSignal.connect(self.getData)
        self.completer = QCompleter([], self.searchEdit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.searchEdit.setCompleter(self.completer)
        self.searchEdit.setClearButtonEnabled(True)
        self.searchEdit.setPlaceholderText("请输入地址")

        # 退出按钮
        self.logoutBtn = PrimaryToolButton()
        self.logoutBtn.setIcon(FIF.POWER_BUTTON)
        self.logoutBtn.clicked.connect(self.handleLogout)
        # 创建表格
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # titleLine
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.addBtn)
        topLayout.addWidget(self.searchEdit)
        topLayout.addStretch()
        topLayout.addWidget(self.logoutBtn)
        self.layout.addLayout(topLayout)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["地址", "创建时间", "操作"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.verticalHeader().setDefaultSectionSize(40)

        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 180)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 60)

        self.layout.addWidget(self.table)
        self.loadData()
        # for i, w in enumerate(wallets):
        #     self.table.setItem(i, 0, QTableWidgetItem(w["address"]))
        #     time_item = QTableWidgetItem(w["created_at"])
        #     time_item.setTextAlignment(Qt.AlignCenter)
        #     self.table.setItem(i, 1, time_item)
        #     # 操作列用空白占位
        #     self.table.setItem(i, 2, QTableWidgetItem(""))

    def createWallet(self):
        data = TronService.generate_wallet()
        address = data.get("address")
        privateKey = data.get("private_key")

        DBService.create_wallet(address, privateKey)
        self.loadData()

    def loadData(self):
        self.data = DBService.list_wallets()
        self.table.setRowCount(len(self.data))
        # 更新搜索补全
        for index, data in enumerate(self.data):
            # 地址列
            itemAddr = QTableWidgetItem(data["address"])
            self.table.setItem(index, 0, itemAddr)

            # 时间列
            itemTime = QTableWidgetItem(data["created_at"])
            itemTime.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(index, 1, itemTime)

            # 操作列按钮
            buttonWidget = QWidget()
            buttonLayout = QHBoxLayout(buttonWidget)
            buttonLayout.setContentsMargins(10, 0, 10, 0)
            buttonLayout.setSpacing(0)

            enterWalletBtn = PrimaryToolButton()
            enterWalletBtn.setIcon(FIF.RIGHT_ARROW)
            enterWalletBtn.setToolTip("进入钱包")
            enterWalletBtn.clicked.connect(partial(self.handleRowAction, index))
            buttonLayout.addWidget(enterWalletBtn, alignment=Qt.AlignCenter)

            self.table.setCellWidget(index, 2, buttonWidget)

    def getData(self):
        pass

    def handleLogout(self):
        pass

    def handleRowAction(self, index):
        print(index)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec())
