#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动观看页面
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QProgressBar,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QRadioButton,
    QFrame,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QGridLayout,
    QToolButton,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QSpinBox,
    QDoubleSpinBox,
    QTimeEdit,
)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTime
from PySide6.QtGui import QIcon

from src.gui.pages.download_page import CourseCardGrid
from src.core.group_manager import GroupManager
from src.core.group import Group
from src.core.task import Task


class TaskCard(QFrame):
    """任务卡片组件，显示单个任务的信息"""

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task: Task = task
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet(
            """
            TaskCard {
                background-color: #ffffff;
                border-radius: 4px;
                margin: 2px;
                padding: 8px;
            }
            QLabel {
                color: #333333;
            }
            QRadioButton {
                margin-right: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #999999;
            }
            QRadioButton::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """
        )
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(15)

        # 创建左侧任务名称容器，固定宽度
        name_container = QWidget()
        name_container.setFixedWidth(400)  # 设置固定宽度
        name_layout = QHBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)

        # 任务名称或ID
        id_label = QLabel(str(self.task.get_name() or self.task.get_task_id()))
        id_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(id_label)
        name_layout.addStretch()  # 添加弹性空间
        layout.addWidget(name_container)

        # 右侧信息容器
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(15)

        # 开始时间
        start_time_label = QLabel(self.task.get_start_time())
        start_time_label.setFixedWidth(100)  # 固定宽度
        info_layout.addWidget(start_time_label)

        # 结束时间
        end_time_label = QLabel(self.task.get_end_time())
        end_time_label.setFixedWidth(100)  # 固定宽度
        info_layout.addWidget(end_time_label)

        # 完成状态
        status_text = "已完成" if self.task.is_finished() else "未完成"
        status_label = QLabel(status_text)
        status_label.setFixedWidth(60)  # 固定宽度
        status_label.setStyleSheet(
            f"color: {'#4CAF50' if self.task.is_finished() else '#FF9800'};"
        )
        info_layout.addWidget(status_label)

        # 选择按钮
        radio_button = QRadioButton()
        radio_button.setChecked(False)
        info_layout.addWidget(radio_button)

        layout.addWidget(info_container)
        layout.addStretch()


class CourseGroupWidget(QWidget):
    """课程组件，显示一个课程的所有任务"""

    def __init__(self, group, show_all_tasks=True, parent=None):
        super().__init__(parent)
        self.group = group
        self.show_all_tasks = show_all_tasks
        self.tasks_layout = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # 课程标题
        title_widget = QWidget()
        title_widget.setStyleSheet(
            """
            QWidget {
                background-color: #f0f0f0;
                border-radius: 4px;
                padding: 5px;
            }
        """
        )
        title_layout = QHBoxLayout(title_widget)
        title_label = QLabel(self.group.get_name())
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_widget)

        # 添加列标题
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setSpacing(15)

        # 名称列标题
        name_header = QWidget()
        name_header.setFixedWidth(400)
        name_header_layout = QHBoxLayout(name_header)
        name_header_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QLabel("名称")
        name_label.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        name_label.setStyleSheet("font-weight: bold; color: #666666;")
        name_header_layout.addWidget(name_label)
        header_layout.addWidget(name_header)

        # 右侧信息列标题
        info_header = QWidget()
        info_header_layout = QHBoxLayout(info_header)
        info_header_layout.setContentsMargins(0, 0, 0, 0)
        info_header_layout.setSpacing(15)

        # 开始时间标题
        start_time_label = QLabel("开始时间")
        start_time_label.setFixedWidth(100)
        start_time_label.setStyleSheet("font-weight: bold; color: #666666;")
        info_header_layout.addWidget(start_time_label)

        # 结束时间标题
        end_time_label = QLabel("结束时间")
        end_time_label.setFixedWidth(100)
        end_time_label.setStyleSheet("font-weight: bold; color: #666666;")
        info_header_layout.addWidget(end_time_label)

        # 状态标题
        status_label = QLabel("状态")
        status_label.setFixedWidth(60)
        status_label.setStyleSheet("font-weight: bold; color: #666666;")
        info_header_layout.addWidget(status_label)

        # 选择标题
        select_label = QLabel("选择")
        select_label.setStyleSheet("font-weight: bold; color: #666666;")
        info_header_layout.addWidget(select_label)

        header_layout.addWidget(info_header)
        header_layout.addStretch()
        layout.addWidget(header_widget)

        # 任务列表容器
        tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(tasks_widget)
        self.tasks_layout.setSpacing(5)
        layout.addWidget(tasks_widget)

        # 初始化任务列表
        self.refresh_tasks()

    def refresh_tasks(self):
        """刷新任务列表"""
        # 清除现有任务
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 获取课程的任务管理器
        task_manager = self.group.get_task_manager()

        if not task_manager.task_list:
            # 如果没有任务，显示提示信息
            if self.show_all_tasks:
                empty_label = QLabel("当前课程暂无任务")
                empty_label.setStyleSheet(
                    "color: #666666; padding: 10px; font-style: italic;"
                )
                self.tasks_layout.addWidget(empty_label)
        else:
            # 创建任务卡片
            has_tasks = False
            for task in task_manager.task_list:
                if self.show_all_tasks or not task.is_finished():
                    task_card = TaskCard(task)
                    self.tasks_layout.addWidget(task_card)
                    has_tasks = True

            # 如果在显示所有任务模式下，所有任务都已完成，显示提示
            if self.show_all_tasks and not has_tasks:
                complete_label = QLabel("所有任务已完成")
                complete_label.setStyleSheet(
                    "color: #4CAF50; padding: 10px; font-weight: bold;"
                )
                self.tasks_layout.addWidget(complete_label)

    def update_display_mode(self, show_all_tasks):
        """更新显示模式"""
        if self.show_all_tasks != show_all_tasks:
            self.show_all_tasks = show_all_tasks
            self.refresh_tasks()


class AutoWatchPage(QWidget):
    """自动观看页面，用于自动完成小雅平台上的视频观看任务"""

    def __init__(self, group_manager=None):
        super().__init__()
        self.group_manager = group_manager
        self.show_all_courses = True  # 是否显示所有任务
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 顶部工具栏
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)

        # 刷新按钮
        refresh_button = QPushButton("刷新任务")
        refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_button.clicked.connect(self._refresh_tasks)
        toolbar_layout.addWidget(refresh_button)

        # 过滤按钮
        self.filter_button = QPushButton("只显示未完成课程")
        self.filter_button.setCheckable(True)
        self.filter_button.clicked.connect(self._toggle_filter)
        self.filter_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:checked {
                background-color: #e0e0e0;
                border: 1px solid #999;
            }
        """
        )
        toolbar_layout.addWidget(self.filter_button)

        toolbar_layout.addStretch()

        # 完成选中任务按钮
        complete_selected_button = QPushButton("完成选中任务")
        complete_selected_button.clicked.connect(self._complete_selected_tasks)
        complete_selected_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        toolbar_layout.addWidget(complete_selected_button)

        # 完成所有任务按钮
        complete_all_button = QPushButton("完成所有任务")
        complete_all_button.clicked.connect(self._complete_all_tasks)
        complete_all_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """
        )
        toolbar_layout.addWidget(complete_all_button)
        layout.addWidget(toolbar)

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建内容容器
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(20)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        # 设置样式
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f5f5f5;
            }
            QScrollArea {
                border: none;
            }
        """
        )

        # 初始加载任务
        self._refresh_tasks()

    @Slot()
    def _toggle_filter(self):
        """切换是否只显示未完成课程"""
        self.show_all_courses = not self.show_all_courses
        self.filter_button.setText(
            "显示所有任务" if not self.show_all_courses else "只显示未完成任务"
        )
        # 重新刷新任务列表
        self._refresh_tasks()

    def _refresh_tasks(self):
        """刷新所有任务"""
        if not self.group_manager:
            return

        # 刷新组管理器
        self.group_manager.refresh_groups()

        # 清除现有内容
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 添加课程组
        for group in self.group_manager.get_all_groups():
            task_manager = group.get_task_manager()
            tasks = task_manager.task_list

            # 在非显示所有模式下，跳过不需要显示的课程
            if not self.show_all_courses:
                if not tasks or all(task.is_finished() for task in tasks):
                    continue

            # 创建课程组件
            course_widget = CourseGroupWidget(
                group, show_all_tasks=self.show_all_courses
            )
            self.content_layout.addWidget(course_widget)

    @Slot()
    def _complete_selected_tasks(self):
        """完成选中的任务"""
        # 查找所有选中的任务
        selected_tasks = []
        for i in range(self.content_layout.count()):
            course_widget = self.content_layout.itemAt(i).widget()
            if isinstance(course_widget, CourseGroupWidget):
                for j in range(course_widget.layout().count()):
                    item = course_widget.layout().itemAt(j).widget()
                    if isinstance(item, QWidget):
                        for child in item.findChildren(TaskCard):
                            radio = child.findChild(QRadioButton)
                            if radio and radio.isChecked():
                                selected_tasks.append(child.task)

        # TODO: 执行完成任务的操作
        if selected_tasks:
            print(f"开始完成 {len(selected_tasks)} 个选中的任务")
            # 这里添加完成任务的具体逻辑

    @Slot()
    def _complete_all_tasks(self):
        """完成所有任务"""
        all_tasks = []
        for i in range(self.content_layout.count()):
            course_widget = self.content_layout.itemAt(i).widget()
            if isinstance(course_widget, CourseGroupWidget):
                task_manager = course_widget.group.get_task_manager()
                for task in task_manager.task_list:
                    if not task.is_finished():
                        all_tasks.append(task)

        # TODO: 执行完成任务的操作
        if all_tasks:
            print(f"开始完成所有 {len(all_tasks)} 个未完成的任务")
            # 这里添加完成任务的具体逻辑

    def update_group_manager(self, group_manager):
        """更新课程管理器"""
        self.group_manager = group_manager
        self._refresh_tasks()
