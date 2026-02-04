"""
-------------------------------------------------
   File Name:        main_widget.py
   Description:      钱包主页面
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
from functools import partial

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QAbstractItemView, QToolBar,
    QMessageBox, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, Signal, QSize

from pages.wallet_widget import WalletWidget
import qtawesome as qta

from service.db_server import DBService
from utils.tron_sdk_service import TronService


class MainWidget(QWidget):
    """主页面"""
    logout_requested = Signal()  # 退出登录信号

    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.w = None
        self.setWindowTitle("Tron 钱包")
        self.data = []
        self.setup_ui()

    def setup_ui(self):
        """创建界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # =========================
        # Toolbar（放在 table 上面）
        # =========================
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(False)  # 不允许拖动
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # 图标+文字

        # Action: 新建
        act_new = QAction(qta.icon('mdi6.plus-circle', color="#1e90ff"), "新建", self)
        act_new.setStatusTip("新建钱包")
        act_new.triggered.connect(lambda: self.create_wallet())
        toolbar.addAction(act_new)

        act_exp = QAction(qta.icon('mdi6.file-export-outline', color="#1e90ff"), "导出", self)
        act_exp.setStatusTip("导出钱包")
        act_exp.triggered.connect(lambda: self.show_msg("点击了：12新建"))
        toolbar.addAction(act_exp)

        # =========================
        # spacer，把退出按钮顶到最右侧
        # =========================
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # 退出按钮
        act_logout = QAction(qta.icon('mdi6.exit-to-app', color="#1e90ff"), "退出", self)
        act_logout.setStatusTip("退出登录")
        act_logout.triggered.connect(self.handle_logout)
        toolbar.addAction(act_logout)

        layout.addWidget(toolbar)

        # =========================
        # Table
        # =========================
        self.table_widget = QTableWidget()
        self.table_widget.setFrameShape(QFrame.NoFrame)
        self.table_widget.setFrameShadow(QFrame.Plain)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["地址", "创建时间", "操作"])
        self.table_widget.horizontalHeader().setStretchLastSection(False)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)

        # 列宽和拖动
        header = self.table_widget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 地址拉伸
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # 创建时间固定
        self.table_widget.setColumnWidth(1, 180)
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # 操作固定
        self.table_widget.setColumnWidth(2, 60)

        layout.addWidget(self.table_widget)

        # 加载示例数据
        self.load_data()

    def create_wallet(self):
        data = TronService.generate_wallet()
        address = data.get("address")
        private_key = data.get("private_key")
        DBService.create_wallet(address, private_key)
        self.load_data()
        QMessageBox.information(self, "提示", "success")

    def show_msg(self, text):
        QMessageBox.information(self, "提示", text)

    def load_data(self):
        """加载示例数据"""
        wallets = DBService.list_wallets()
        print(wallets)
        self.table_widget.setRowCount(len(wallets))

        for row, data in enumerate(wallets):
            # 地址
            item_addr = QTableWidgetItem(data["address"])
            self.table_widget.setItem(row, 0, item_addr)

            # 创建时间
            item_time = QTableWidgetItem(data["created_at"])
            item_time.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 1, item_time)

            # 操作按钮
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(10, 0, 10, 0)
            button_layout.setSpacing(0)

            action_button = QPushButton("连接")
            action_button.clicked.connect(partial(self.handle_row_action, row))

            button_layout.addWidget(action_button, alignment=Qt.AlignCenter)
            self.table_widget.setCellWidget(row, 2, button_widget)

    def handle_row_action(self, row):
        """处理行操作按钮点击"""
        self.w = WalletWidget()
        self.w.show()
        print(f"点击了第 {row + 1} 行的操作按钮")

    def handle_logout(self):
        """处理退出登录"""
        self.logout_requested.emit()
        self.close()

    def get_data(self):
        self.data = []
