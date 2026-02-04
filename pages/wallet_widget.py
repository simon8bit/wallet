import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QMessageBox
)
import qtawesome as qta


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
        self.btn_transfer.setIcon(qta.icon("mdi6.send"))
        self.btn_transfer.setIconSize(QSize(16, 16))

        self.btn_history = QPushButton("记录")
        self.btn_history.setIcon(qta.icon("mdi6.history"))
        self.btn_history.setIconSize(QSize(16, 16))

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
        self.resize(520, 360)
        self.row = row
        self.assets = [
            {"symbol": "TRX", "balance": "0.0000"},
            {"symbol": "USDT", "balance": "0.0000"},
            {"symbol": "HE", "balance": "0.0000"},
        ]

        self.setup_ui()
        self.load_assets()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # 顶部栏（原生 QLabel + QPushButton）
        top_layout = QHBoxLayout()
        self.title = QLabel(f"钱包地址 {self.row.get("address", "")}")
        self.btn_refresh = QPushButton("刷新")
        self.btn_refresh.setIcon(qta.icon("mdi6.refresh"))
        self.btn_refresh.clicked.connect(self.refresh_assets)

        top_layout.addWidget(self.title)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(top_layout)

        # 列表
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.NoSelection)  # 不可选中
        self.list_widget.setSpacing(2)  # 行间距（原生效果）

        main_layout.addWidget(self.list_widget, 1)

    def load_assets(self):
        self.list_widget.clear()

        for asset in self.assets:
            row_widget = AssetRowWidget(asset["symbol"], asset["balance"])

            item = QListWidgetItem()
            item.setSizeHint(row_widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, row_widget)

    def refresh_assets(self):
        # 模拟刷新
        for a in self.assets:
            if a["symbol"] == "TRX":
                a["balance"] = "12.3456"
            elif a["symbol"] == "USDT":
                a["balance"] = "0.3000"
            else:
                a["balance"] = "88.0000"

        self.load_assets()
        QMessageBox.information(self, "刷新", "余额已刷新（模拟）")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WalletWidget()
    w.show()
    sys.exit(app.exec())
