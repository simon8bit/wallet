import sys
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget,
    QMessageBox
)
import qtawesome as qta


class AssetRowWidget(QWidget):
    """每一行资产：币种 + 余额 + 转账按钮 + 记录按钮"""

    def __init__(self, symbol: str, balance: str, parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.balance = balance

        # ------------------------
        # 主布局
        # ------------------------
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        # ------------------------
        # 左侧：币种图标 + 名称
        # ------------------------
        self.icon_label = QLabel()
        icon_map = {
            "TRX": "mdi6.wallet-plus-outline",
            "HE": "mdi6.wallet-plus-outline",
            "USDT": "mdi6.wallet-plus-outline"
        }
        icon_name = icon_map.get(symbol, "mdi6.currency-usd")
        self.icon_label.setPixmap(qta.icon(icon_name, color="#ff8c00").pixmap(24, 24))

        self.lbl_symbol = QLabel(symbol)
        self.lbl_symbol.setStyleSheet("font-weight: bold; font-size: 14px; color: #333333;")

        symbol_layout = QHBoxLayout()
        symbol_layout.addWidget(self.icon_label)
        symbol_layout.addWidget(self.lbl_symbol)
        symbol_layout.addStretch()

        # ------------------------
        # 中间：余额
        # ------------------------
        self.lbl_balance = QLabel(balance)
        self.lbl_balance.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_balance.setStyleSheet("font-size: 14px; color: #1a1a1a; font-weight: 500;")

        # ------------------------
        # 右侧按钮：转账、记录
        # ------------------------
        self.btn_transfer = QPushButton("转账")
        self.btn_history = QPushButton("记录")
        btn_icons = {
            self.btn_transfer: "mdi6.arrow-top-right",
            self.btn_history: "mdi6.history"
        }

        for btn in (self.btn_transfer, self.btn_history):
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(30)
            btn.setIcon(qta.icon(btn_icons[btn], color="#1e90ff"))
            # btn.setStyleSheet("""
            #     QPushButton {
            #         border: 1px solid #1e90ff;
            #         color: #1e90ff;
            #         border-radius: 6px;
            #         padding: 4px 12px;
            #         font-size: 13px;
            #     }
            #     QPushButton:hover {
            #         background-color: #1e90ff;
            #         color: white;
            #     }
            # """)

        self.btn_transfer.clicked.connect(self.on_transfer)
        self.btn_history.clicked.connect(self.on_history)

        # ------------------------
        # 添加到主布局
        # ------------------------
        layout.addLayout(symbol_layout)
        layout.addWidget(self.lbl_balance, 1)
        layout.addWidget(self.btn_transfer)
        layout.addWidget(self.btn_history)

    def on_transfer(self):
        QMessageBox.information(self, "转账", f"准备给 {self.symbol} 转账")

    def on_history(self):
        QMessageBox.information(self, "记录", f"查看 {self.symbol} 的交易记录")


class WalletWidget(QWidget):
    """钱包主界面"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tron 钱包")
        self.setMinimumSize(400, 260)
        self.setup_ui()
        self.center_window()

    def center_window(self):
        """窗口居中显示"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def setup_ui(self):
        """创建界面"""
        main_layout = QVBoxLayout(self)
        for i in range(3):
            main_layout.addWidget(QListWidget())


# -----------------------------
# Demo 运行
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WalletWidget()
    w.show()
    sys.exit(app.exec())
