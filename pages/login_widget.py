"""
-------------------------------------------------
   File Name:        login_widget.py
   Description:      钱包登录界面（简洁版）
   Author:           simon
   Version:          3.0
-------------------------------------------------
"""
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem
from qfluentwidgets import (PushButton, LineEdit)


class LoginWidget(QWidget):
    """登录页面（简洁版）"""
    login_success = Signal(str, str)  # 用户名, 密码

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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # ========================
        # 标题
        # ========================
        title = QLabel("Tron 钱包")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("安全、便捷的数字资产管理")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        # 间距
        main_layout.addSpacing(10)

        # ========================
        # 用户名输入框
        # ========================
        self.username_input = LineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setMinimumWidth(250)
        self.username_input.setMinimumHeight(32)
        main_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # ========================
        # 密码输入框
        # ========================
        self.password_input = LineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(LineEdit.Password)
        self.password_input.setMinimumWidth(250)
        self.password_input.setMinimumHeight(32)
        self.password_input.returnPressed.connect(self.handle_login)
        main_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # ========================
        # 登录按钮
        # ========================
        self.login_button = PushButton("登录")
        self.login_button.setMinimumWidth(250)
        self.login_button.setMinimumHeight(36)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # ========================
        # 提示信息
        # ========================
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.info_label)

        # ========================
        # 弹性间距
        # ========================
        main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            self.info_label.setText("请输入用户名")
            self.username_input.setFocus()
            return

        if not password:
            self.info_label.setText("请输入密码")
            self.password_input.setFocus()
            return

        # 清空提示
        self.info_label.setText("")

        # 登录成功信号
        self.login_success.emit(username, password)
