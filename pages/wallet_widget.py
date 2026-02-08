import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QMessageBox
)
import qtawesome as qta
from service.async_get_balance import AsyncRequestBalance
import datetime


class AssetRowWidget(QWidget):
    """每一行资产：币种 + 余额 + 转账按钮 + 记录按钮（原生风格）"""

    def __init__(self, symbol: str, balance: str, parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.balance = balance

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # 图标
        self.icon_label = QLabel()
        icon_map = {
            "TRX": "mdi6.lightning-bolt",
            "HE": "mdi6.wallet-outline",
            "USDT": "mdi6.currency-usd"
        }
        icon_name = icon_map.get(symbol, "mdi6.currency-usd")
        self.icon_label.setPixmap(qta.icon(icon_name).pixmap(22, 22))

        # 币种名
        self.lbl_symbol = QLabel(symbol)
        self.lbl_symbol.setMinimumWidth(60)

        # 余额
        self.lbl_balance = QLabel(balance)
        self.lbl_balance.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 按钮
        self.btn_transfer = QPushButton("转账")
        # self.btn_transfer.setIcon(qta.icon("mdi6.send"))
        # self.btn_transfer.setIconSize(QSize(16, 16))

        self.btn_history = QPushButton("记录")
        # self.btn_history.setIcon(qta.icon("mdi6.history"))
        # self.btn_history.setIconSize(QSize(16, 16))

        self.btn_transfer.clicked.connect(self.on_transfer)
        self.btn_history.clicked.connect(self.on_history)

        # 布局
        layout.addWidget(self.icon_label)
        layout.addWidget(self.lbl_symbol)
        layout.addWidget(self.lbl_balance, 1)
        layout.addWidget(self.btn_transfer)
        layout.addWidget(self.btn_history)

    def set_balance(self, balance: str):
        self.balance = balance
        self.lbl_balance.setText(balance)

    def on_transfer(self):
        QMessageBox.information(self, "转账", f"准备给 {self.symbol} 转账")

    def on_history(self):
        QMessageBox.information(self, "记录", f"查看 {self.symbol} 的交易记录")


class WalletWidget(QWidget):
    """钱包主界面（原生风格）"""

    def __init__(self, row):
        super().__init__()
        self.setWindowTitle("Tron 钱包")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(520, 360)
        self.row = row
        self.req_thread = AsyncRequestBalance(self.row.get("address"))
        self.req_thread.success.connect(self.on_load_success)
        self.req_thread.error.connect(self.on_load_error)
        self.req_thread.start()

        # 总体布局
        self.main_layout = QVBoxLayout(self)
        # self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(10)
        # //title控件
        self.title = QLabel(f"钱包地址 {self.row.get("address", "")}")
        self.btn_refresh = QPushButton("连接中...")
        self.btn_refresh.setFixedWidth(80)
        self.btn_refresh.setStyleSheet("background-color:transparent;")
        self.btn_refresh.setIcon(QIcon("statics/loading.png"))

        self.btn_refresh.clicked.connect(self.refresh_assets)
        # title的布局

        self.main_layout.addWidget(self.title)
        self.refresh_info = QLabel()
        self.main_layout.addWidget(self.refresh_info)
        self.main_layout.addWidget(self.btn_refresh)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.NoSelection)  # 不可选中
        self.list_widget.setSpacing(2)  # 行间距（原生效果）

        self.main_layout.addWidget(self.list_widget, 1)
        self.main_layout.addStretch()

        self.setup_ui()

    def on_load_success(self, result):
        assets = [
            {"symbol": "TRX", "balance": "1.0000"},
            {"symbol": "USDT", "balance": "2.0000"},
        ]
        self.refresh_info.setText(f"更新时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.load_assets(assets)
        self.btn_refresh.setText("刷新")
        self.btn_refresh.setIcon(qta.icon("mdi6.refresh"))
        print(f"result1:{result}")

    def on_load_error(self, result):
        assets = [
            {"symbol": "TRX", "balance": "0.0000"},
            {"symbol": "USDT", "balance": "0.0000"},
        ]
        self.refresh_info.setText(f"更新时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.load_assets(assets)
        self.btn_refresh.setText("刷新")
        self.btn_refresh.setIcon(qta.icon("mdi6.refresh"))
        print(f"result2:{result}")
        QMessageBox.information(
            self, "请求", result)

    def setup_ui(self):
        self.label = QLabel("查询错误")
        # 列表

    def load_assets(self, assets):
        self.list_widget.clear()
        for asset in assets:
            row_widget = AssetRowWidget(asset["symbol"], asset["balance"])
            item = QListWidgetItem()
            item.setSizeHint(row_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, row_widget)

    def refresh_assets(self):
        self.btn_refresh.setText("刷新中...")
        self.btn_refresh.setIcon(QIcon("statics/loading.png"))
        self.req_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WalletWidget()
    w.show()
    sys.exit(app.exec())
