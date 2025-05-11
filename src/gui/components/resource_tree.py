#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源树组件，用于显示课程资源的树形结构
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QFrame
)
from PySide6.QtCore import Qt, Signal

from .resource_item import ResourceItem


class ResourceTree(QWidget):
    """资源树组件"""
    
    itemCheckStateChanged = Signal(str, bool)  # 项目选中状态改变信号
    itemDownloadRequested = Signal(str)  # 项目下载请求信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items_map = {}  # 存储所有项目的映射
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建树形控件
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # 隐藏表头
        self.tree.setFrameStyle(QFrame.NoFrame)  # 无边框
        self.tree.setIndentation(0)  # 禁用默认缩进
        self.tree.setVerticalScrollMode(QTreeWidget.ScrollPerPixel)  # 平滑滚动
        
        # 设置样式
        self.tree.setStyleSheet("""
            QTreeWidget {
                background: transparent;
                border: none;
            }
            QTreeWidget::item {
                padding: 5px 0;
                border-bottom: 1px solid #E5E5E5;
            }
            QTreeWidget::item:selected {
                background: transparent;
            }
        """)
        
        layout.addWidget(self.tree)
        
    def add_resource(self, path, is_folder=False, parent_path=None):
        """添加资源项
        
        Args:
            path: 资源路径
            is_folder: 是否为文件夹
            parent_path: 父级路径
        """
        name = path.split('/')[-1]
        level = len(path.split('/')) - 1
        
        # 创建树项
        tree_item = QTreeWidgetItem()
        if parent_path:
            parent_item = self.items_map.get(parent_path)
            if parent_item:
                parent_item['tree_item'].addChild(tree_item)
            else:
                self.tree.addTopLevelItem(tree_item)
        else:
            self.tree.addTopLevelItem(tree_item)
            
        # 创建资源项组件
        resource_item = ResourceItem(name, is_folder, level)
        resource_item.checkStateChanged.connect(
            lambda checked: self._on_item_checked(path, checked))
        if not is_folder:
            resource_item.downloadClicked.connect(
                lambda: self.itemDownloadRequested.emit(path))
            
        self.tree.setItemWidget(tree_item, 0, resource_item)
        
        # 存储项目信息
        self.items_map[path] = {
            'tree_item': tree_item,
            'resource_item': resource_item,
            'is_folder': is_folder,
            'children': []
        }
        
        # 更新父项的子项列表
        if parent_path and parent_path in self.items_map:
            self.items_map[parent_path]['children'].append(path)
            
        return tree_item
        
    def _on_item_checked(self, path, checked):
        """处理项目选中状态改变"""
        item_info = self.items_map.get(path)
        if not item_info:
            return
            
        # 如果是文件夹，递归设置所有子项的状态
        if item_info['is_folder']:
            self._set_children_check_state(path, checked)
            
        # 更新父文件夹的状态
        self._update_parent_check_state(path)
        
        # 发送信号
        self.itemCheckStateChanged.emit(path, checked)
        
    def _set_children_check_state(self, path, checked):
        """递归设置子项的选中状态"""
        item_info = self.items_map.get(path)
        if not item_info:
            return
            
        for child_path in item_info['children']:
            child_info = self.items_map.get(child_path)
            if child_info:
                child_info['resource_item'].set_checked(checked)
                if child_info['is_folder']:
                    self._set_children_check_state(child_path, checked)
                    
    def _update_parent_check_state(self, path):
        """更新父文件夹的选中状态"""
        parent_path = '/'.join(path.split('/')[:-1])
        if not parent_path or parent_path not in self.items_map:
            return
            
        parent_info = self.items_map[parent_path]
        if not parent_info['is_folder']:
            return
            
        # 检查所有子项的状态
        all_checked = True
        any_checked = False
        
        for child_path in parent_info['children']:
            child_info = self.items_map.get(child_path)
            if child_info and child_info['resource_item'].is_checked():
                any_checked = True
            else:
                all_checked = False
                
        # 设置父文件夹的状态
        parent_info['resource_item'].set_checked(all_checked)
        
        # 递归更新上级文件夹
        self._update_parent_check_state(parent_path)
        
    def get_checked_items(self):
        """获取所有选中的项目"""
        checked_items = []
        for path, info in self.items_map.items():
            if not info['is_folder'] and info['resource_item'].is_checked():
                checked_items.append(path)
        return checked_items
        
    def set_all_checked(self, checked):
        """设置所有项目的选中状态"""
        for path, info in self.items_map.items():
            if not info['is_folder']:
                info['resource_item'].set_checked(checked)
