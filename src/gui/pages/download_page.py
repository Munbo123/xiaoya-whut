#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源下载页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QProgressBar, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QCheckBox, QGroupBox, QRadioButton, QFrame,
    QScrollArea, QSplitter, QTabWidget, QGridLayout, QToolButton, QDialog,
    QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy, QStackedWidget,
    QFormLayout
)
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon

from src.gui.components.course_card import CourseCard

class CourseCardGrid(QWidget):
    """课程卡片网格视图"""
    
    courseSelected = Signal(str)  # 课程被选择时发出信号
    courseActionTriggered = Signal(str, str)  # 课程操作被触发时发出信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout(self)
        
        # 课程筛选区域
        filter_layout = QHBoxLayout()
        
        # 学期筛选
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("全部学期")
        self.semester_combo.addItem("2025年春")
        self.semester_combo.addItem("2024年秋")
        filter_layout.addWidget(QLabel("学期:"))
        filter_layout.addWidget(self.semester_combo)
        
        # 状态筛选
        self.status_combo = QComboBox()
        self.status_combo.addItem("全部状态")
        self.status_combo.addItem("进行中")
        self.status_combo.addItem("已结束")
        filter_layout.addWidget(QLabel("状态:"))
        filter_layout.addWidget(self.status_combo)
        
        # 关键字搜索
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索课程名称或教师")
        self.search_btn = QPushButton("搜索")
        self.search_btn.setIcon(QIcon.fromTheme("search"))
        filter_layout.addWidget(self.search_edit)
        filter_layout.addWidget(self.search_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        filter_layout.addWidget(self.refresh_btn)
        
        self.layout.addLayout(filter_layout)
        
        # 课程卡片滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(15)
        
        scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(scroll_area)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_courses)
        self.refresh_btn.clicked.connect(self.refresh_courses)
        self.semester_combo.currentTextChanged.connect(self.filter_courses)
        self.status_combo.currentTextChanged.connect(self.filter_courses)
        
        # 加载示例数据
        self.load_example_data()
        
    def load_example_data(self):
        """加载示例数据，实际项目中这里会从服务器获取数据"""
        example_courses = [
            {
                "id": "course1", 
                "name": "程序设计综合实验", 
                "teacher": "刘传文", 
                "semester": "2025年春", 
                "dept": "学院: 计算机智能学院",
                "views": 811,
                "students": 85
            },
            {
                "id": "course2", 
                "name": "初级羽毛球", 
                "teacher": "文湘南", 
                "semester": "2025年春", 
                "dept": "学院: 体育学院",
                "views": 548,
                "students": 272
            },
            {
                "id": "course3", 
                "name": "大国三农II——农业科技版(GX)", 
                "teacher": "智慧网络辅导", 
                "semester": "2025年春", 
                "dept": "学院: 本科生院",
                "views": 303,
                "students": 120
            },
            {
                "id": "course4", 
                "name": "计算机网络", 
                "teacher": "李春林,康星", 
                "semester": "2025年春", 
                "dept": "学院: 计算机智能学院",
                "views": 1700,
                "students": 71
            },
            {
                "id": "course5", 
                "name": "计算机学科前沿讲座", 
                "teacher": "王超", 
                "semester": "2025年春", 
                "dept": "学院: 计算机智能学院",
                "views": 600,
                "students": 128
            },
            {
                "id": "course6", 
                "name": "计算机组成原理理论设计", 
                "teacher": "张三", 
                "semester": "2025年春", 
                "dept": "学院: 计算机智能学院",
                "views": 423,
                "students": 96
            }
        ]
        
        self.clear_grid()
        
        # 添加课程卡片
        row, col = 0, 0
        max_cols = 3  # 每行最多显示3个卡片
        
        for course in example_courses:
            card = CourseCard(
                course_id=course["id"],
                course_name=course["name"],
                teacher_name=course["teacher"],
                semester=course["semester"],
                dept_name=course["dept"],
                views=course["views"],
                students=course["students"]
            )
            
            # 连接卡片信号
            card.clicked.connect(self.on_course_selected)
            card.actionTriggered.connect(self.on_course_action)
            
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
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
    
    @Slot(str, str)
    def on_course_action(self, course_id, action):
        """课程操作被触发"""
        self.courseActionTriggered.emit(course_id, action)
    
    @Slot()
    def search_courses(self):
        """搜索课程"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            return
            
        # 实际项目中这里会进行真正的搜索
        # 示例中仅显示提示信息
        print(f"搜索: {search_text}")
    
    @Slot()
    def refresh_courses(self):
        """刷新课程列表"""
        # 实际项目中这里会重新从服务器获取数据
        # 示例中重新加载示例数据
        self.load_example_data()
    
    @Slot(str)
    def filter_courses(self, text):
        """根据学期或状态筛选课程"""
        # 实际项目中这里会应用筛选
        # 示例中简单地重新加载数据
        self.load_example_data()


class ResourceDownloadDialog(QDialog):
    """资源下载对话框，显示所选课程的资源列表和下载选项"""
    
    def __init__(self, course_id, course_name, parent=None):
        super().__init__(parent)
        
        self.course_id = course_id
        self.course_name = course_name
        
        self.setWindowTitle(f"下载资源 - {course_name}")
        self.resize(800, 600)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 课程信息标题
        title_label = QLabel(f"课程: {self.course_name}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 资源类型选择标签页
        self.tab_widget = QTabWidget()
        
        # 课件标签页
        self.courseware_tab = QWidget()
        self.tab_widget.addTab(self.courseware_tab, "课件")
        
        # 视频标签页
        self.video_tab = QWidget()
        self.tab_widget.addTab(self.video_tab, "视频")
        
        # 试题标签页
        self.quiz_tab = QWidget()
        self.tab_widget.addTab(self.quiz_tab, "试题")
        
        # 其他资源标签页
        self.other_tab = QWidget()
        self.tab_widget.addTab(self.other_tab, "其他资源")
        
        layout.addWidget(self.tab_widget)
        
        # 设置各个标签页内容
        self._setup_resource_tab(self.courseware_tab, "课件")
        self._setup_resource_tab(self.video_tab, "视频")
        self._setup_resource_tab(self.quiz_tab, "试题")
        self._setup_resource_tab(self.other_tab, "其他资源")
        
        # 下载选项区域
        options_group = QGroupBox("下载选项")
        options_layout = QHBoxLayout(options_group)
        
        self.download_path_edit = QLineEdit()
        self.download_path_edit.setReadOnly(True)
        self.download_path_edit.setPlaceholderText("下载保存路径")
        self.browse_btn = QPushButton("浏览...")
        self.select_all_btn = QPushButton("全选")
        self.select_none_btn = QPushButton("取消全选")
        self.download_btn = QPushButton("下载选中资源")
        self.download_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        options_layout.addWidget(QLabel("保存路径:"))
        options_layout.addWidget(self.download_path_edit, 1)
        options_layout.addWidget(self.browse_btn)
        options_layout.addWidget(self.select_all_btn)
        options_layout.addWidget(self.select_none_btn)
        options_layout.addWidget(self.download_btn)
        
        layout.addWidget(options_group)
        
        # 进度区域
        progress_group = QGroupBox("下载进度")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.status_label = QLabel("就绪")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        
        # 连接信号
        self.browse_btn.clicked.connect(self.browse_save_path)
        self.download_btn.clicked.connect(self.download_resources)
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_none_btn.clicked.connect(self.select_none)
    
    def _setup_resource_tab(self, tab_widget, resource_type):
        """设置资源标签页的内容"""
        layout = QVBoxLayout(tab_widget)
        
        # 资源列表
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(4)
        self.resource_table.setHorizontalHeaderLabels(["选择", "资源名称", "类型", "大小"])
        self.resource_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # 添加示例数据
        row_count = 5
        self.resource_table.setRowCount(row_count)
        for i in range(row_count):
            checkbox = QCheckBox()
            self.resource_table.setCellWidget(i, 0, checkbox)
            self.resource_table.setItem(i, 1, QTableWidgetItem(f"{resource_type}示例 {i+1}"))
            self.resource_table.setItem(i, 2, QTableWidgetItem("PDF" if i % 2 == 0 else "PPT"))
            self.resource_table.setItem(i, 3, QTableWidgetItem(f"{(i+1)*2} MB"))
        
        layout.addWidget(self.resource_table)
    
    def browse_save_path(self):
        """浏览保存路径"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择下载保存路径", 
            "C:/",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            self.download_path_edit.setText(folder)
    
    def select_all(self):
        """全选当前标签页的所有资源"""
        current_tab = self.tab_widget.currentWidget()
        table = current_tab.findChild(QTableWidget)
        if table:
            for i in range(table.rowCount()):
                checkbox = table.cellWidget(i, 0)
                if checkbox and isinstance(checkbox, QCheckBox):
                    checkbox.setChecked(True)
    
    def select_none(self):
        """取消全选当前标签页的资源"""
        current_tab = self.tab_widget.currentWidget()
        table = current_tab.findChild(QTableWidget)
        if table:
            for i in range(table.rowCount()):
                checkbox = table.cellWidget(i, 0)
                if checkbox and isinstance(checkbox, QCheckBox):
                    checkbox.setChecked(False)
    
    def download_resources(self):
        """下载选中资源（示例）"""
        current_tab = self.tab_widget.currentWidget()
        table = current_tab.findChild(QTableWidget)
        if not table:
            return
            
        selected_count = 0
        for i in range(table.rowCount()):
            checkbox = table.cellWidget(i, 0)
            if checkbox and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                selected_count += 1
        
        if selected_count == 0:
            self.status_label.setText("请选择要下载的资源")
            return
        
        save_path = self.download_path_edit.text()
        if not save_path:
            self.status_label.setText("请选择保存路径")
            return
        
        # 实际中这里会有下载逻辑
        self.status_label.setText(f"开始下载 {selected_count} 个资源...")
        self.progress_bar.setValue(50)  # 示例进度


class DownloadPage(QWidget):
    """资源下载页面，用于下载小雅平台上的课程资源"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        
        # 添加标题
        title_label = QLabel("资源下载")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 课程卡片网格视图 - 直接显示，不再需要登录
        self.course_grid = CourseCardGrid()
        
        # 连接课程卡片信号
        self.course_grid.courseSelected.connect(self.on_course_selected)
        self.course_grid.courseActionTriggered.connect(self.on_course_action)
        
        # 添加课程网格到主布局
        main_layout.addWidget(self.course_grid)
    
    @Slot(str)
    def on_course_selected(self, course_id):
        """课程被选择的处理函数"""
        # 示例处理，实际中可能会有其他操作
        print(f"课程被选择: {course_id}")
    
    @Slot(str, str)
    def on_course_action(self, course_id, action):
        """课程操作被触发的处理函数"""
        if action == "download":
            # 找到对应的课程卡片以获取课程名称
            for i in range(self.course_grid.grid_layout.count()):
                item = self.course_grid.grid_layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), CourseCard) and item.widget().course_id == course_id:
                    course_name = item.widget().course_name
                    # 打开资源下载对话框
                    dialog = ResourceDownloadDialog(course_id, course_name, self)
                    dialog.exec()
                    break
        elif action == "auto_watch":
            print(f"自动观看: {course_id}")
        elif action == "detail":
            print(f"查看详情: {course_id}")