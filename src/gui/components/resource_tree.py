#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源树组件，用于显示课程资源并支持下载
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, 
    QTreeWidgetItem, QHeaderView, QStyle, QStyledItemDelegate,
    QApplication
)
from PySide6.QtCore import Qt, Signal, QSize, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
import qtawesome as qta

class ResourceItemDelegate(QStyledItemDelegate):
    """自定义代理，用于绘制选择框和下载按钮"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkbox_rect = QRect(0, 0, 20, 20)
        self.download_icon = qta.icon('fa5s.download', color='#666666')
        
    def paint(self, painter: QPainter, option, index):
        """绘制项目"""
        # 保存画笔状态
        painter.save()
        
        # 获取项目数据
        item = index.model().itemFromIndex(index)
        is_checked = item.checkState() == Qt.Checked
        
        # 绘制选择框
        checkbox_rect = QRect(
            option.rect.left() + 4,
            option.rect.center().y() - 10,
            20, 20
        )
        
        painter.setPen(QPen(QColor("#666666")))
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(checkbox_rect)
        
        if is_checked:
            inner_rect = QRect(
                checkbox_rect.left() + 4,
                checkbox_rect.top() + 4,
                12, 12
            )
            painter.setBrush(QBrush(QColor("#0369a1")))
            painter.drawEllipse(inner_rect)
        
        # 绘制文本
        text_rect = QRect(
            option.rect.left() + 30,
            option.rect.top(),
            option.rect.width() - 60,
            option.rect.height()
        )
        painter.drawText(text_rect, Qt.AlignVCenter, index.data())
        
        # 绘制下载按钮
        if not item.childCount():  # 只有文件才显示下载按钮
            download_rect = QRect(
                option.rect.right() - 30,
                option.rect.center().y() - 10,
                20, 20
            )
            self.download_icon.paint(painter, download_rect)
        
        painter.restore()

    def editorEvent(self, event, model, option, index):
        """处理鼠标事件"""
        return super().editorEvent(event, model, option, index)

class ResourceTreeWidget(QWidget):
    """资源树组件"""
    
    download_requested = Signal(list)  # 下载请求信号，传递选中的资源列表
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建工具栏
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(10)
        
        # 创建按钮
        self.select_all_btn = QPushButton("全选")
        self.select_none_btn = QPushButton("全不选")
        self.download_selected_btn = QPushButton("下载选中资源")
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: #374151;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
            QPushButton:pressed {
                background-color: #D1D5DB;
            }
        """
        self.select_all_btn.setStyleSheet(button_style)
        self.select_none_btn.setStyleSheet(button_style)
        self.download_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #0369a1;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        
        # 添加按钮到工具栏
        toolbar.addWidget(self.select_all_btn)
        toolbar.addWidget(self.select_none_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.download_selected_btn)
        
        # 创建树形控件
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(20)
        self.tree.setIconSize(QSize(16, 16))
        self.tree.setAnimated(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #E5E7EB;
                border-radius: 4px;
                background: white;
            }
            QTreeWidget::item {
                height: 30px;
                padding-right: 10px;
            }
            QTreeWidget::item:hover {
                background: #F3F4F6;
            }
        """)
        
        # 设置自定义代理
        self.tree_delegate = ResourceItemDelegate(self.tree)
        self.tree.setItemDelegate(self.tree_delegate)
        
        # 添加到主布局
        layout.addLayout(toolbar)
        layout.addWidget(self.tree)
        
        # 连接信号
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_none_btn.clicked.connect(self.select_none)
        self.download_selected_btn.clicked.connect(self.download_selected)
        self.tree.itemClicked.connect(self.handle_item_clicked)
        self.tree.itemChanged.connect(self.handle_item_changed)
    
    def add_resources(self, resources):
        """添加资源到树形控件"""
        self.tree.clear()
        self._add_resources_recursive(resources, self.tree.invisibleRootItem())
        
    def _add_resources_recursive(self, resources, parent_item):
        """递归添加资源"""
        for resource in resources:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, resource['name'])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Unchecked)
            
            if 'children' in resource:
                self._add_resources_recursive(resource['children'], item)
                item.setIcon(0, qta.icon('fa5s.folder', color='#666666'))
            else:
                item.setIcon(0, qta.icon('fa5s.file', color='#666666'))
                item.setData(0, Qt.UserRole, resource.get('url', ''))
    
    def select_all(self):
        """全选"""
        self._set_check_state_recursive(self.tree.invisibleRootItem(), Qt.Checked)
    
    def select_none(self):
        """全不选"""
        self._set_check_state_recursive(self.tree.invisibleRootItem(), Qt.Unchecked)
    
    def _set_check_state_recursive(self, item, state):
        """递归设置选中状态"""
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, state)
            if child.childCount() > 0:
                self._set_check_state_recursive(child, state)
    
    def _get_selected_resources(self, item):
        """递归获取选中的资源"""
        resources = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.checkState(0) == Qt.Checked:
                url = child.data(0, Qt.UserRole)
                if url:  # 如果是文件
                    resources.append({
                        'name': child.text(0),
                        'url': url
                    })
            if child.childCount() > 0:
                resources.extend(self._get_selected_resources(child))
        return resources
    
    def download_selected(self):
        """下载选中的资源"""
        selected = self._get_selected_resources(self.tree.invisibleRootItem())
        if selected:
            self.download_requested.emit(selected)
    
    def handle_item_clicked(self, item, column):
        """处理项目点击事件"""
        # 检查是否点击了选择框区域
        pos = self.tree.viewport().mapFromGlobal(QApplication.mousePos())
        checkbox_rect = QRect(
            self.tree.visualItemRect(item).left() + 4,
            self.tree.visualItemRect(item).center().y() - 10,
            20, 20
        )
        
        if checkbox_rect.contains(pos):
            new_state = Qt.Unchecked if item.checkState(0) == Qt.Checked else Qt.Checked
            item.setCheckState(0, new_state)
            # 递归设置子项目的状态
            if item.childCount() > 0:
                self._set_check_state_recursive(item, new_state)
        
        # 检查是否点击了下载按钮区域
        download_rect = QRect(
            self.tree.visualItemRect(item).right() - 30,
            self.tree.visualItemRect(item).center().y() - 10,
            20, 20
        )
        
        if download_rect.contains(pos) and item.childCount() == 0:
            url = item.data(0, Qt.UserRole)
            if url:
                self.download_requested.emit([{
                    'name': item.text(0),
                    'url': url
                }])
    
    def handle_item_changed(self, item, column):
        """处理项目状态改变事件"""
        if column == 0:
            # 更新父项目的状态
            parent = item.parent()
            if parent:
                checked_count = 0
                total_count = parent.childCount()
                
                for i in range(total_count):
                    if parent.child(i).checkState(0) == Qt.Checked:
                        checked_count += 1
                
                if checked_count == total_count:
                    parent.setCheckState(0, Qt.Checked)
                elif checked_count == 0:
                    parent.setCheckState(0, Qt.Unchecked)
                else:
                    parent.setCheckState(0, Qt.PartiallyChecked)
