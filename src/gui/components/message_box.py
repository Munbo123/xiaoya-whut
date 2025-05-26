#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义消息框组件
提供在深色和浅色模式下都能正常显示的各种消息框
"""

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon


class MessageBox:
    """
    自定义消息框类
    提供在深色和浅色模式下都能正常显示的各种消息框
    """

    @staticmethod
    def information(
        parent, title, text, buttons=QMessageBox.Ok, default_button=QMessageBox.Ok
    ):
        """
        显示信息消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本
            buttons: 按钮组合
            default_button: 默认按钮

        Returns:
            int: 用户点击的按钮值
        """
        return MessageBox._show_message_box(
            parent, title, text, QMessageBox.Information, buttons, default_button
        )

    @staticmethod
    def warning(
        parent, title, text, buttons=QMessageBox.Ok, default_button=QMessageBox.Ok
    ):
        """
        显示警告消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本
            buttons: 按钮组合
            default_button: 默认按钮

        Returns:
            int: 用户点击的按钮值
        """
        return MessageBox._show_message_box(
            parent, title, text, QMessageBox.Warning, buttons, default_button
        )

    @staticmethod
    def critical(
        parent, title, text, buttons=QMessageBox.Ok, default_button=QMessageBox.Ok
    ):
        """
        显示错误消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本
            buttons: 按钮组合
            default_button: 默认按钮

        Returns:
            int: 用户点击的按钮值
        """
        return MessageBox._show_message_box(
            parent, title, text, QMessageBox.Critical, buttons, default_button
        )

    @staticmethod
    def question(
        parent,
        title,
        text,
        buttons=QMessageBox.Yes | QMessageBox.No,
        default_button=QMessageBox.No,
    ):
        """
        显示询问消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本
            buttons: 按钮组合，默认为"是/否"
            default_button: 默认按钮，默认为"否"

        Returns:
            int: 用户点击的按钮值
        """
        return MessageBox._show_message_box(
            parent, title, text, QMessageBox.Question, buttons, default_button
        )

    @staticmethod
    def about(parent, title, text):
        """
        显示关于消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本

        Returns:
            int: 用户点击的按钮值
        """
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        MessageBox._apply_style(msg)
        return msg.exec_()

    @staticmethod
    def _show_message_box(parent, title, text, icon, buttons, default_button):
        """
        显示自定义消息框

        Args:
            parent: 父窗口
            title: 标题
            text: 显示文本
            icon: 图标类型
            buttons: 按钮组合
            default_button: 默认按钮

        Returns:
            int: 用户点击的按钮值
        """
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(buttons)
        msg.setDefaultButton(default_button)

        # 应用样式
        MessageBox._apply_style(msg)

        return msg.exec_()

    @staticmethod
    def _apply_style(msg_box):
        """
        应用消息框样式

        Args:
            msg_box: QMessageBox对象
        """
        # 设置消息框大小
        msg_box.setMinimumWidth(400)

        # 应用样式表
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #bbbbbb;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border: 1px solid #bbbbbb;
            }
            QPushButton:default {
                background-color: #2196F3;
                color: white;
                border: 1px solid #1976D2;
            }
            QPushButton:default:hover {
                background-color: #1976D2;
            }
            QPushButton:default:pressed {
                background-color: #0D47A1;
            }
        """
        )
