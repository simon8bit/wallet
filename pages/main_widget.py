from functools import partial
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QAbstractItemView, QHeaderView,
    QTableWidgetItem, QCompleter, QSizePolicy
)

from pages.wallet_widget import WalletWidget
from service.db_server import DBService
from utils.tron_sdk_service import TronService

from qfluentwidgets import (
    PrimaryPushButton, PrimaryToolButton,
    VBoxLayout, TableWidget, MessageBox,
    SearchLineEdit
)
from qfluentwidgets import FluentIcon as FIF


class MainWidget(QWidget):
    """主页面"""

    logoutRequested = Signal()  # 退出登录信号

    def __init__(self, username=None):
        super().__init__()

        self.username = username
        self.walletWindow = None
        self.rows = []

        self.setWindowTitle("Tron 钱包")

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

        # 表格
        self.tableWidget = TableWidget()
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["地址", "创建时间", "操作"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)

        # 设置每行高度
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)

        # 设置列宽
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(1, 180)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(2, 60)

        self.setupUi()

    def getData(self, text: str):
        print("搜索内容:", text)
        # 可根据 text 过滤钱包列表
        filtered = [
            w for w in DBService.list_wallets() if text in w["address"]
        ]
        self.loadData(filtered)

    def setupUi(self):
        """创建界面"""
        layout = VBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 顶部按钮和搜索
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.addBtn)
        topLayout.addWidget(self.searchEdit)
        topLayout.addStretch()
        topLayout.addWidget(self.logoutBtn)
        layout.addLayout(topLayout)

        # 表格拉伸占满剩余空间
        layout.addWidget(self.tableWidget)

        # 加载初始数据
        self.loadData()

    def createWallet(self):
        data = TronService.generate_wallet()
        address = data.get("address")
        privateKey = data.get("private_key")

        DBService.create_wallet(address, privateKey)
        self.loadData()

        MessageBox.information(self, "创建成功", f"钱包地址：\n{address}")

    def loadData(self, wallets=None):
        """加载数据"""
        if wallets is None:
            wallets = DBService.list_wallets()
        self.rows = wallets

        self.tableWidget.setRowCount(len(wallets))

        # 更新搜索补全
        addresses = [w["address"] for w in wallets]
        self.completer.model().setStringList(addresses)

        for index, data in enumerate(wallets):
            # 地址列
            itemAddr = QTableWidgetItem(data["address"])
            self.tableWidget.setItem(index, 0, itemAddr)

            # 时间列
            itemTime = QTableWidgetItem(data["created_at"])
            itemTime.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(index, 1, itemTime)

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

            self.tableWidget.setCellWidget(index, 2, buttonWidget)

    def handleRowAction(self, index: int):
        row = self.rows[index]
        self.walletWindow = WalletWidget(row)
        self.walletWindow.show()

    def handleLogout(self):
        self.logoutRequested.emit()
        self.close()
