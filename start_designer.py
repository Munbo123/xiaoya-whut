#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动Qt Designer的Python脚本
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def find_designer():
    """
    查找Qt Designer的可执行文件路径
    """
    # 1. 尝试在PySide6包中查找
    try:
        import PySide6
        designer_path = Path(PySide6.__file__).parent / "designer.exe"
        if designer_path.exists():
            return str(designer_path)
    except ImportError:
        print("未安装PySide6，尝试其他路径...")
    
    # 2. 尝试在系统PATH中查找
    designer_name = "designer.exe" if platform.system() == "Windows" else "designer"
    designer_path = shutil.which(designer_name)
    if designer_path:
        return designer_path
    
    # 3. 尝试在常见的Qt安装目录查找
    common_paths = []
    if platform.system() == "Windows":
        common_paths = [
            r"C:\Qt\*\*\bin\designer.exe",
            r"C:\Qt\Tools\*\bin\designer.exe",
            r"C:\Program Files\Qt\*\bin\designer.exe",
            r"C:\Program Files (x86)\Qt\*\bin\designer.exe"
        ]
    elif platform.system() == "Darwin":  # macOS
        common_paths = [
            "/Applications/Qt*/*/bin/Designer.app/Contents/MacOS/Designer",
            "/usr/local/opt/qt/bin/designer"
        ]
    else:  # Linux
        common_paths = [
            "/usr/bin/designer",
            "/usr/local/bin/designer",
            "/opt/qt*/bin/designer"
        ]
    
    import glob
    for pattern in common_paths:
        paths = glob.glob(pattern)
        if paths:
            return max(paths)  # 返回版本最高的Qt Designer
    
    return None


def main():
    """
    主函数，启动Qt Designer
    """
    print("正在查找Qt Designer...")
    designer_path = find_designer()
    
    if designer_path:
        print(f"找到Qt Designer: {designer_path}")
        print("正在启动Qt Designer...")
        try:
            result = subprocess.run([designer_path], check=True)
            sys.exit(result.returncode)
        except subprocess.CalledProcessError as e:
            print(f"启动Qt Designer失败: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"无法执行 {designer_path}，文件不存在或无法访问")
            sys.exit(1)
    else:
        print("未能找到Qt Designer。")
        print("请确保已安装Qt和PySide6，或者将Qt Designer添加到系统PATH中。")
        sys.exit(1)


if __name__ == "__main__":
    main()