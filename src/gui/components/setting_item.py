from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QLineEdit,
    QComboBox,
    QCheckBox,
)
import qtawesome as qta
from PySide6.QtCore import Signal, Qt


class SettingItem(QWidget):
    # 定义信号
    valueChanged = Signal()  # 值改变信号

    def __init__(
        self,
        name: str,
        icon: "qta.icon_painter.IconType" = None,
        description: str = "",
        value=None,
        sub_settings: list["SettingItem"] = None,
        value_type=None,
        options: list[str] = None,
    ):
        """
        设置项类
        :param name: 设置项名称
        :param icon: 设置项图标
        :param description: 设置项描述
        :param value: 设置项值
        :param sub_settings: 子设置项列表
        :param value_type: 设置项值的类型
        :param options: 期望的值列表（用于下拉框）
        """
        super().__init__(parent=None)

        self.icon = icon if icon else qta.icon("fa5s.cog", color="black")  # 默认图标
        self.name = name
        self.description = description
        self.sub_settings = sub_settings if sub_settings else []
        # 设置的种类，如按钮，输入框，下拉框,滑动按钮等
        self.value_type = value_type
        self.value = value
        self.options = options if options else []
        self.control = None  # 控件实例

        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(0)

        # 创建主Frame
        self.frame = QFrame()
        self.frame.setStyleSheet(
            """
            QFrame {
                background-color: #F3F4F6;
                border-radius: 8px;
            }
            QFrame:hover {
                background-color: #E5E7EB;
            }
        """
        )
        self.frame.setFixedHeight(56)  # 减小高度使布局更紧凑

        # 水平主布局
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setContentsMargins(10, 0, 12, 0)
        frame_layout.setSpacing(10)

        # 图标布局
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.pixmap(22))  # 使用更小的图标
        icon_label.setFixedSize(22, 22)
        icon_label.setStyleSheet("margin: 0;")
        frame_layout.addWidget(icon_label, 0, Qt.AlignVCenter)

        # 文本部分
        text_container = QWidget()
        text_container.setStyleSheet("background: transparent;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 8, 0, 8)
        text_layout.setSpacing(1)  # 极小的间距

        # 标题
        name_label = QLabel(self.name)
        name_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            color: #374151;
            margin: 0;
            padding: 0;
        """
        )
        text_layout.addWidget(name_label)

        # 描述
        desc_label = QLabel(self.description)
        desc_label.setStyleSheet(
            """
            font-size: 12px;
            color: #6B7280;
            margin: 0;
            padding: 0;
        """
        )
        text_layout.addWidget(desc_label)

        frame_layout.addWidget(text_container, 0, Qt.AlignVCenter)
        frame_layout.addStretch(1)  # 弹性空间

        # 控件部分
        if self.value_type == QPushButton:
            # 值显示文本框
            self.value_display = QLineEdit(self.value if self.value else "")
            self.value_display.setStyleSheet(
                """
                QLineEdit {
                    border: 1px solid #D1D5DB;
                    border-radius: 4px;
                    padding: 5px 8px;
                    background: white;
                    min-width: 260px;
                    max-width: 400px;
                    color: #374151;
                }
                QLineEdit:hover {
                    border-color: #9CA3AF;
                }
            """
            )
            self.value_display.setReadOnly(True)
            frame_layout.addWidget(self.value_display)

            # 选择按钮
            self.control = QPushButton("选择")
            self.control.setStyleSheet(
                """
                QPushButton {
                    background-color: #4B5563;
                    color: white;
                    border-radius: 4px;
                    padding: 5px 12px;
                    font-size: 13px;
                    min-width: 70px;
                    max-width: 70px;
                }
                QPushButton:hover {
                    background-color: #374151;
                }
            """
            )
            self.control.clicked.connect(self._on_value_changed)
            frame_layout.addWidget(self.control)
        elif self.value_type == QComboBox:
            # 下拉框
            self.control = QComboBox()
            if self.value not in self.options:
                self.options.insert(0, self.value)
            self.control.setStyleSheet(
                """
                QComboBox {
                    border: 1px solid #D1D5DB;
                    border-radius: 4px;
                    padding: 4px 8px;
                    min-width: 120px;
                    background: white;
                }
                QComboBox:hover {
                    border-color: #9CA3AF;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                    border-left-width: 1px;
                    border-left-color: #D1D5DB;
                    border-left-style: solid;
                }
                QComboBox::down-arrow {
                    image: url(assets/pictures/arrow_down.png);
                    width: 10px;
                    height: 10px;
                }
            """
            )
            self.control.addItems(self.options)
            # 由于已经把value添加到expect_values中，所以index一定存在
            index = self.control.findText(self.value)
            self.control.setCurrentIndex(index)
            self.control.currentTextChanged.connect(self._on_value_changed)
            frame_layout.addWidget(self.control)

        elif self.value_type == QCheckBox:
            self.control = QCheckBox()
            self.control.setStyleSheet(
                """
                QCheckBox {
                    spacing: 4px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 1px solid #D1D5DB;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    background-color: #4B5563;
                    border-color: #4B5563;
                }
            """
            )
            self.control.setChecked(bool(self.value))
            self.control.stateChanged.connect(self._on_value_changed)
            frame_layout.addWidget(self.control)

        elif self.value_type == QLineEdit:
            self.control = QLineEdit(self.value if self.value else "")
            self.control.setStyleSheet(
                """
                QLineEdit {
                    border: 1px solid #D1D5DB;
                    border-radius: 4px;
                    padding: 4px 8px;
                    min-width: 180px;
                    background: white;
                }
                QLineEdit:hover {
                    border-color: #9CA3AF;
                }
                QLineEdit:focus {
                    border-color: #6B7280;
                }
            """
            )
            self.control.textChanged.connect(self._on_value_changed)
            frame_layout.addWidget(self.control)

        layout.addWidget(self.frame)


    def _on_value_changed(self):
        """值改变处理"""
        # 内部状态同步 - 确保self.value反映控件的当前值
        if isinstance(self.control, QComboBox):
            self.value = self.control.currentText()
        elif isinstance(self.control, QLineEdit):
            self.value = self.control.text()
        elif isinstance(self.control, QCheckBox):
            self.value = self.control.isChecked()
        
        # 然后发送信号，通知外部状态已变化
        self.valueChanged.emit()

    def set_icon(self, icon: "qta.icon_painter.IconType"):
        """设置图标"""
        self.icon = icon

    def set_name(self, name: str):
        """设置名称"""
        self.name = name

    def set_description(self, description: str):
        """设置描述"""
        self.description = description

    def set_value(self, value: str):
        """
        设置值并更新控件显示
        :param value: 新的值
        """
        self.value = value
        # 更新控件显示的值
        if self.control:
            if isinstance(self.control, QLineEdit):
                self.control.setText(value)
            elif isinstance(self.control, QComboBox):
                index = self.control.findText(value)
                if index >= 0:
                    self.control.setCurrentIndex(index)
            elif isinstance(self.control, QCheckBox):
                self.control.setChecked(bool(value))
            elif isinstance(self.control, QPushButton):
                # 只更新路径显示框的值，保持按钮文本不变
                if hasattr(self, "path_display"):
                    self.path_display.setText(value)

    def update_options(self, new_options: list[str], keep_current_value=True):
        """
        更新下拉框选项
        
        Args:
            new_options: 新的选项列表
            keep_current_value: 是否保留当前选中的值
        """
        if not isinstance(self.control, QComboBox):
            return False
            
        current = self.control.currentText() if keep_current_value else None
        
        # 更新内部选项列表
        self.options = new_options.copy()
        
        # 清空并添加新选项
        self.control.blockSignals(True)  # 暂时阻止信号触发
        self.control.clear()
        
        # 如果当前值不在新选项中但需要保留，添加到选项中
        if current and keep_current_value and current not in self.options:
            self.options.insert(0, current)
        
        self.control.addItems(self.options)
        
        # 恢复选中状态
        if current and keep_current_value:
            index = self.control.findText(current)
            if index >= 0:
                self.control.setCurrentIndex(index)
        elif self.options:
            self.control.setCurrentIndex(0)
            self.value = self.options[0]
            
        self.control.blockSignals(False)
        return True

    def set_sub_settings(self, sub_settings: list["SettingItem"]):
        """设置子设置项"""
        self.sub_settings = sub_settings

    def get_icon(self):
        """获取图标"""
        return self.icon

    def get_name(self):
        """获取名称"""
        return self.name

    def get_description(self):
        """获取描述"""
        return self.description

    def get_value(self):
        """获取值"""
        return self.value

    def get_sub_settings(self):
        """获取子设置项"""
        return self.sub_settings

    def get_value_type(self):
        """获取值的类型"""
        return self.value_type

    def get_options(self) -> list[str]:
        """获取当前下拉框的所有选项"""
        if isinstance(self.control, QComboBox):
            return [self.control.itemText(i) for i in range(self.control.count())]
        return self.options.copy()

    def add_sub_setting(self, sub_setting: "SettingItem"):
        """添加子设置项"""
        self.sub_settings.append(sub_setting)

    def __str__(self):
        return f"SettingItem(name={self.name})"

    def __repr__(self):
        return f"SettingItem(name={self.name}, value={self.value})"
