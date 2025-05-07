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
from PySide6.QtGui import QIcon, QMovie

from src.gui.components.course_card import CourseCard

class CourseCardGrid(QWidget):
    """课程卡片网格视图"""
    
    courseSelected = Signal(str)  # 课程被选择时发出信号
    courseActionTriggered = Signal(str, str)  # 课程操作被触发时发出信号
    
    def __init__(self, course_manager=None, parent=None):
        super().__init__(parent)
        self.course_manager = course_manager
        self.loading = False
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout(self)
        
        # 课程筛选区域
        filter_layout = QHBoxLayout()
        
        # 学期筛选
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("全部学期")
        if self.course_manager:
            for term in self.course_manager.get_all_terms():
                self.semester_combo.addItem(term)
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
        
        # 创建堆叠布局，用于切换课程网格和加载状态
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack, 1)  # 1表示stretch因子

        # 课程卡片滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
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
        self.loading_text.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                margin-top: 10px;
            }
        """)
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
        enabled = not self.loading and self.course_manager is not None
        self.search_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        self.semester_combo.setEnabled(enabled)
        self.status_combo.setEnabled(enabled)
        self.search_edit.setEnabled(enabled)

    def load_courses(self):
        """从CourseManager加载课程数据"""
        self.show_loading()
        self.clear_grid()
        
        if not self.course_manager:
            self.show_loading("请登录以获取课程信息")
            return
            
        courses = self.course_manager.get_all_courses()
        if not courses:
            self.show_loading("暂无课程信息")
            return
            
        # 应用过滤器
        semester = self.semester_combo.currentText()
        status = self.status_combo.currentText()
        search_text = self.search_edit.text().strip().lower()
        
        # 过滤课程
        if semester != "全部学期":
            courses = [c for c in courses if c.get_term() == semester]
            
        if status != "全部状态":
            if status == "进行中":
                courses = [c for c in courses if c.is_active()]
            else:
                courses = [c for c in courses if not c.is_active()]
                
        if search_text:
            courses = [c for c in courses if 
                      search_text in c.get_name().lower() or 
                      any(search_text in t.lower() for t in c.get_teachers())]
        
        # 如果筛选后没有课程
        if not courses:
            self.show_loading("未找到符合条件的课程")
            return

        # 添加课程卡片
        row, col = 0, 0
        max_cols = 3  # 每行最多显示3个卡片
        
        for course in courses:
            card = CourseCard(
                course_id=course.get_id(),
                course_name=course.get_name(),
                teacher_name=", ".join(course.get_teachers()),
                semester=course.get_term(),
                dept_name=course.get_department(),
                views=course.get_visit_number(),
                students=course.get_member_count(),
                image_path=course.get_cover_img()
            )
            
            # 连接卡片信号
            card.clicked.connect(self.on_course_selected)
            card.actionTriggered.connect(self.on_course_action)
            
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
    
    @Slot(str, str)
    def on_course_action(self, course_id, action):
        """课程操作被触发"""
        self.courseActionTriggered.emit(course_id, action)
    
    @Slot()
    def search_courses(self):
        """搜索课程"""
        self.load_courses()
    
    @Slot()
    def refresh_courses(self):
        """刷新课程列表"""
        if self.course_manager:
            self.course_manager.refresh_courses()
        self.load_courses()
    
    @Slot(str)
    def filter_courses(self, text):
        """根据学期或状态筛选课程"""
        self.load_courses()


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
    
    def __init__(self, course_manager=None):
        super().__init__()
        self.course_manager = course_manager
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
        
        # 课程卡片网格视图
        self.course_grid = CourseCardGrid(self.course_manager)
        
        # 连接课程卡片信号
        self.course_grid.courseSelected.connect(self.on_course_selected)
        self.course_grid.courseActionTriggered.connect(self.on_course_action)
        
        # 添加课程网格到主布局
        main_layout.addWidget(self.course_grid)
    
    @Slot(str)
    def on_course_selected(self, course_id):
        """课程被选择的处理函数"""
        if not self.course_manager:
            return
        course = self.course_manager.get_course_by_id(course_id)
        if course:
            print(f"课程被选择: {course.get_name()}")
    
    @Slot(str, str)
    def on_course_action(self, course_id, action):
        """课程操作被触发的处理函数"""
        if not self.course_manager:
            return
            
        course = self.course_manager.get_course_by_id(course_id)
        if not course:
            return
            
        if action == "download":
            # 打开资源下载对话框
            dialog = ResourceDownloadDialog(course_id, course.get_name(), self)
            dialog.exec()
        elif action == "auto_watch":
            print(f"自动观看: {course.get_name()}")
        elif action == "detail":
            print(f"查看详情: {course.get_name()}")