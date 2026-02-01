"""
-------------------------------------------------
   File Name:        main_widget.py
   Description:      钱包主页面
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from datetime import datetime


class MainWidget(QWidget):
    """主页面"""
    logout_requested = Signal()  # 退出登录信号
    
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setWindowTitle("Tron 钱包 - 主页面")
        self.data = []
        self.setup_ui()
        
    def setup_ui(self):
        """创建界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部布局（标题和退出按钮）
        top_layout = QHBoxLayout()
        
        # 欢迎标题
        if self.username:
            welcome_text = f"欢迎，{self.username}！"
        else:
            welcome_text = "欢迎使用 Tron 钱包"
            
        title = QLabel(welcome_text)
        title.setAlignment(Qt.AlignCenter)
        
        # 退出按钮
        exit_button = QPushButton("退出")
        exit_button.clicked.connect(self.handle_logout)
        
        top_layout.addWidget(title, 1)  # 标题占据剩余空间
        top_layout.addWidget(exit_button)  # 退出按钮在右边
        
        layout.addLayout(top_layout)
        
        # 表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["地址", "TRX", "USDT", "刷新时间", "操作"])
        
        # 设置表格属性
        self.table_widget.horizontalHeader().setStretchLastSection(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)  # 禁用行选择
        
        # 设置列宽（私钥和地址列需要更宽）
        header = self.table_widget.horizontalHeader()
        header.setSectionsMovable(True)  # 允许拖动列（可选：换顺序）
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 地址列拉伸
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # TRX列自适应
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # USDT列自适应
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 刷新时间列自适应
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # 操作列固定宽度
        header.resizeSection(4, 100)  # 操作列宽度固定为100

        layout.addWidget(self.table_widget)
        
        # 加载示例数据
        self.load_sample_data()

    def load_sample_data(self):
        """加载示例数据"""
        sample_data = [
            {
                "address": "TXYZabcdefghijklmnopqrstuvwxyz123456",
                "private_key": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
                "trx": "100.50",
                "usdt": "500.25",
                "create_time": "2024-01-15 10:30:00",
                "refresh_time": "2024-01-20 14:25:00"
            },
            {
                "address": "TABCdefghijklmnopqrstuvwxyz987654",
                "private_key": "f1e2d3c4b5a6789012345678901234567890fedcba1234567890fedcba123456",
                "trx": "250.75",
                "usdt": "1200.50",
                "create_time": "2024-01-16 09:15:00",
                "refresh_time": "2024-01-20 15:30:00"
            },
            {
                "address": "TJKLMnopqrstuvwxyzabcdefghijklmno012",
                "private_key": "9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba",
                "trx": "1000.00",
                "usdt": "5000.00",
                "create_time": "2024-01-19 08:00:00",
                "refresh_time": "2024-01-20 18:15:00"
            },
            {
                "address": "TJKLMnopqrstuvwxyzabcdefghijklmno012",
                "private_key": "9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba",
                "trx": "1000.00",
                "usdt": "5000.00",
                "create_time": "2024-01-19 08:00:00",
                "refresh_time": "2024-01-20 18:15:00"
            }
        ]
        
        self.table_widget.setRowCount(len(sample_data))
        
        for row, data in enumerate(sample_data):
            # 地址
            item = QTableWidgetItem(data["address"])
            self.table_widget.setItem(row, 0, item)
            
            # 私钥
            # item = QTableWidgetItem(data["private_key"])
            # self.table_widget.setItem(row, 1, item)
            
            # TRX
            item = QTableWidgetItem(data["trx"])
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table_widget.setItem(row, 1, item)
            
            # USDT
            item = QTableWidgetItem(data["usdt"])
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table_widget.setItem(row, 2, item)
            
            # 刷新时间
            item = QTableWidgetItem(data["refresh_time"])
            item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 3, item)
            
            # 操作按钮（最后一列）
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(10, 0, 10, 0)  # 左右边距各10
            button_layout.setSpacing(0)
            
            action_button = QPushButton("操作")
            action_button.setFixedWidth(80)  # 按钮宽度固定为80
            action_button.clicked.connect(lambda checked, r=row: self.handle_row_action(r))
            button_layout.addWidget(action_button)
            
            self.table_widget.setCellWidget(row, 4, button_widget)
    
    def handle_row_action(self, row):
        """处理行操作按钮点击"""
        # 这里可以添加具体的操作逻辑
        print(f"点击了第 {row + 1} 行的操作按钮")
    
    def handle_logout(self):
        """处理退出登录"""
        self.logout_requested.emit()
        self.close()
    
    def get_data(self):
        self.data = []
