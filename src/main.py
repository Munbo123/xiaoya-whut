#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
小雅平台助手核心逻辑模块
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到系统路径，确保可以导入其他模块
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon

# 导入自定义模块
from src.gui.main_window import MainWindow
from src.core.app_config import AppConfig

def setup_application():
    """设置应用程序基本信息和环境"""
    # 设置应用信息
    QCoreApplication.setApplicationName("小雅平台助手")
    QCoreApplication.setApplicationVersion("2.0")
    QCoreApplication.setOrganizationName("xiaoya-whut")
    
    # 配置高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # 配置应用图标
    app_icon_path = os.path.join(project_root, "assets", "pictures", "Appicon.ico")
    if os.path.exists(app_icon_path):
        app_icon = QIcon(app_icon_path)
        QApplication.setWindowIcon(app_icon)

def main():
    """
    程序主入口函数，处理核心业务逻辑
    """
    # 创建Qt应用实例
    app = QApplication(sys.argv)
    
    # 设置应用程序基本信息
    setup_application()
    
    # 加载配置
    config = AppConfig()
    config.load_config()
    
    # 初始化主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 执行应用程序事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    # 当直接运行此文件时也可以启动程序
    main()