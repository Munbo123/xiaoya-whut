#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程卡片网格视图组件
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QFrame,
    QScrollArea,
    QStackedWidget,
    QGridLayout,
)
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QMovie
import qtawesome as qta

from src.gui.components.course_card import CourseCard
from src.core.group import Group


class CourseCardGrid(QWidget):
    """课程卡片网格视图"""

    courseSelected = Signal(str)  # 课程被选择时发出信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_manager = parent.group_manager if parent else None
        self.login_manager = parent.login_manager if parent else None
        self.user_info_manager = parent.user_info_manager if parent else None
        self.loading = False
        self.init_ui()

        # 初始加载课程数据
        self.load_courses()

    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout(self)

        # 课程筛选区域
        filter_layout = QHBoxLayout()

        # 学期筛选
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("全部学期")
        self.semester_combo.setStyleSheet(
            """
            QComboBox {
                color: #333;
                font-size: 14px;
                padding: 5px;
                background-color: #F0F0F0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #F0F0F0;
                color: #333;
                selection-background-color: #0369a1;
                selection-color: white;
                border: 1px solid #ccc;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #ccc;
                background-color: #E0E0E0;
            }

            QComboBox::down-arrow {
                image: url(./assets/pictures/arrow_down.png);
                width: 12px;
                height: 12px;
            }
        """
        )

        if self.group_manager:
            for term in self.group_manager.get_all_terms():
                self.semester_combo.addItem(term)
        label1 = QLabel("学期:")
        label1.setStyleSheet("font-size: 14px; color: #333;")
        filter_layout.addWidget(label1)
        filter_layout.addWidget(self.semester_combo)

        # 状态筛选
        self.status_combo = QComboBox()
        self.status_combo.setStyleSheet(
            """
            QComboBox {
                color: #333;
                font-size: 14px;
                padding: 5px;
                background-color: #F0F0F0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #F0F0F0;
                color: #333;
                selection-background-color: #0369a1;
                selection-color: white;
                border: 1px solid #ccc;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #ccc;
                background-color: #E0E0E0;
            }

            QComboBox::down-arrow {
                image: url(./assets/pictures/arrow_down.png);
                width: 12px;
                height: 12px;
            }
        """
        )
        self.status_combo.addItem("全部状态")
        self.status_combo.addItem("进行中")
        self.status_combo.addItem("已结束")
        label2 = QLabel("状态:")
        label2.setStyleSheet("font-size: 14px; color: #333;")
        filter_layout.addWidget(label2)
        filter_layout.addWidget(self.status_combo)

        # 关键字搜索
        self.search_edit = QLineEdit()
        self.search_edit.setStyleSheet(
            """
            QLineEdit {
                color: #333;
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #66afe9;
            }
        """
        )
        self.search_edit.setPlaceholderText("搜索课程名称或教师")

        self.search_btn = QPushButton("搜索")
        self.search_btn.setStyleSheet(
            """
            QPushButton {
                color: #fff;
                background-color: #007bff;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """
        )
        self.search_btn.setIcon(QIcon.fromTheme("search"))
        filter_layout.addWidget(self.search_edit)
        filter_layout.addWidget(self.search_btn)
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                color: #fff;
                background-color: #28a745;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """
        )
        # 使用qtawesome设置白色刷新图标
        refresh_icon = qta.icon("fa5s.sync", color="white")
        self.refresh_btn.setIcon(refresh_icon)
        filter_layout.addWidget(self.refresh_btn)

        self.layout.addLayout(filter_layout)

        # 创建堆叠布局，用于切换课程网格和加载状态
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack, 1)  # 1表示stretch因子

        # 课程卡片滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
        )

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(15)

        self.scroll_area.setWidget(self.scroll_content)
        self.stack.addWidget(self.scroll_area)

        # 加载状态显示页面
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)

        # 加载动画
        self.spinner = QLabel()
        loading_layout.addWidget(self.spinner, 0, Qt.AlignCenter)

        # 加载提示文字
        self.loading_text = QLabel()
        self.loading_text.setStyleSheet(
            """
            QLabel {
                color: #666666;
                font-size: 14px;
                margin-top: 10px;
            }
        """
        )
        loading_layout.addWidget(self.loading_text, 0, Qt.AlignCenter)

        self.stack.addWidget(self.loading_widget)

        # 连接信号
        self.search_btn.clicked.connect(self.search_courses)
        self.refresh_btn.clicked.connect(self.refresh_courses)
        self.semester_combo.currentTextChanged.connect(self.filter_courses)
        self.status_combo.currentTextChanged.connect(self.filter_courses)

        # 初始化加载状态
        self.setup_loading_animation()
        self.show_loading("请登录以获取课程信息")

    def setup_loading_animation(self):
        """设置加载动画"""
        # 创建加载动画
        movie = QMovie("assets/pictures/loading.gif")
        movie.setScaledSize(QSize(48, 48))
        self.spinner.setMovie(movie)
        movie.start()

    def show_loading(self, text="加载中..."):
        """显示加载状态"""
        self.loading = True
        self.loading_text.setText(text)
        self.stack.setCurrentWidget(self.loading_widget)
        self.update_buttons_state()

    def hide_loading(self):
        """隐藏加载状态"""
        self.loading = False
        self.stack.setCurrentWidget(self.scroll_area)
        self.update_buttons_state()

    def update_buttons_state(self):
        """更新按钮状态"""
        enabled = not self.loading and self.group_manager is not None
        self.search_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        self.semester_combo.setEnabled(enabled)
        self.status_combo.setEnabled(enabled)
        self.search_edit.setEnabled(enabled)

    def load_courses(self):
        """从GroupManager加载课程数据"""
        self.show_loading()
        self.clear_grid()

        if not self.group_manager:
            self.show_loading("请登录以获取课程信息")
            return

        groups: list[Group] = self.group_manager.get_all_groups()
        if not groups:
            self.show_loading("暂无课程信息")
            return

        # 应用过滤器
        semester = self.semester_combo.currentText()
        status = self.status_combo.currentText()
        search_text = self.search_edit.text().strip().lower()

        # 过滤课程组
        if semester != "全部学期":
            groups = [g for g in groups if g.get_term() == semester]

        if status != "全部状态":
            if status == "进行中":
                groups = [g for g in groups if g.is_active()]
            else:
                groups = [g for g in groups if not g.is_active()]

        if search_text:
            groups = [
                g
                for g in groups
                if search_text in g.get_name().lower()
                or any(search_text in t.lower() for t in g.get_teachers())
            ]

        # 如果筛选后没有课程
        if not groups:
            self.show_loading("未找到符合条件的课程")
            return

        # 添加课程卡片
        row, col = 0, 0
        max_cols = 3  # 每行最多显示3个卡片

        for group in groups:
            card = CourseCard(
                course_id=group.get_id(),
                course_name=group.get_name(),
                teacher_name=", ".join(group.get_teachers()),
                semester=group.get_term(),
                dept_name=group.get_department(),
                views=group.get_visit_number(),
                students=group.get_member_count(),
                image_path=group.get_cover_img(),
            )

            # 连接卡片信号
            card.clicked.connect(self.on_course_selected)

            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # 显示课程卡片
        self.hide_loading()

    def clear_grid(self):
        """清空网格布局中的所有卡片"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    @Slot(str)
    def on_course_selected(self, course_id):
        """课程被选择"""
        self.courseSelected.emit(course_id)

    @Slot()
    def search_courses(self):
        """搜索课程"""
        self.load_courses()

    @Slot()
    def refresh_courses(self):
        """刷新课程列表"""
        if self.group_manager:
            self.group_manager.refresh_groups()
        self.load_courses()

    @Slot(str)
    def filter_courses(self, text):
        """根据学期或状态筛选课程"""
        self.load_courses()

    def update_group_manager(self, group_manager):
        """更新课程管理器"""
        self.group_manager = group_manager
        self.load_courses()

    def update_login_manager(self, login_manager):
        """更新登录管理器"""
        self.login_manager = login_manager

    def update_user_info_manager(self, user_info_manager):
        """更新用户信息管理器"""
        self.user_info_manager = user_info_manager
