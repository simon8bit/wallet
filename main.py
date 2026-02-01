"""
-------------------------------------------------
   File Name:        main.py
   Description:      Tron 钱包主程序入口
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from pages.login_widget import LoginWidget
from pages.main_widget import MainWidget


def main():
    """主函数 - 启动钱包应用"""
    app = QApplication(sys.argv)
    
    # 设置全局字体大小（影响所有控件的默认大小）
    # 可以通过调整字体大小来全局调整控件大小
    font = QFont()
    font.setPointSize(8)  # 默认字体大小，可以调整这个值来改变控件大小
    app.setFont(font)
    
    # 创建登录窗口
    login_window = LoginWidget()
    login_window.show()
    
    # 保存主窗口引用，防止被垃圾回收
    main_window = None
    
    # 处理登录成功信号，跳转到主界面
    def on_login_success(username, password):
        nonlocal main_window, login_window
        # 创建主页面
        main_window = MainWidget(username)
        main_window.setMinimumSize(1000, 600)
        main_window.show()
        # 关闭登录窗口
        login_window.close()
        
        # 处理退出登录信号，返回登录界面
        def on_logout():
            nonlocal login_window, main_window
            main_window.close()
            # 重新创建登录窗口
            login_window = LoginWidget()
            login_window.show()
            login_window.login_success.connect(on_login_success)
        
        main_window.logout_requested.connect(on_logout)
    
    login_window.login_success.connect(on_login_success)
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
