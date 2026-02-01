"""
-------------------------------------------------
   File Name:        login_widget.py
   Description:      钱包登录界面
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton, 
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal


class LoginWidget(QWidget):
    """登录页面"""
    login_success = Signal(str, str)  # 用户名, 密码
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tron")
        self.setFixedSize(400, 280)
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
        
        # 标题
        title = QLabel("Tron 钱包(安全、便捷的数字资产管理)")
        title.setFont(QFont("Arial", 10))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        subtitle = QLabel("安全、便捷的数字资产管理")
        subtitle.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(subtitle)
        
        # 添加一些间距
        main_layout.addSpacing(10)
        
        # 表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setHorizontalSpacing(15)
        
        # 用户名输入
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setMinimumHeight(32)
        self.username_input.setMinimumWidth(250)
        form_layout.addRow("用户名：", self.username_input)
        
        # 密码输入
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(32)
        self.password_input.setMinimumWidth(250)
        form_layout.addRow("密码：", self.password_input)
        
        # 回车键登录
        self.password_input.returnPressed.connect(self.handle_login)
        
        main_layout.addLayout(form_layout)
        
        # 添加一些间距
        main_layout.addSpacing(10)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setMinimumHeight(36)
        self.login_button.setMinimumWidth(120)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        
        # 提示信息
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setMinimumHeight(20)
        main_layout.addWidget(self.info_label)
        
        main_layout.addStretch()
        
    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # 验证输入
        if not username:
            QMessageBox.warning(self, "提示", "请输入用户名")
            self.username_input.setFocus()
            return
            
        if not password:
            QMessageBox.warning(self, "提示", "请输入密码")
            self.password_input.setFocus()
            return
        
        # 显示登录成功提示
        QMessageBox.information(self, "登录成功", f"欢迎，{username}！")
        
        # 发送登录成功信号
        self.login_success.emit(username, password)
