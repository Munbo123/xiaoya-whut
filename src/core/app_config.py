#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用配置管理模块
"""

import os
import json
from pathlib import Path


class AppConfig:
    """应用程序配置类，负责管理和存储用户配置"""
    
    def __init__(self):
        # 配置文件路径
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.config_file = self.config_dir / "app_config.json"
        
        # 默认配置
        self.default_config = {
            "username": "",
            "password": "",
            "auto_login": False,
            "save_path": str(Path.home() / "Downloads" / "xiaoya_downloads"),
            "theme": "light",
            "notification": True,
            "auto_start": False
        }
        
        # 当前配置
        self.config = self.default_config.copy()
    
    def load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        try:
            # 确保配置目录存在
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True)
            
            # 如果配置文件不存在，创建默认配置
            if not self.config_file.exists():
                self.save_config()
                return
            
            # 读取配置
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                
            # 将加载的配置与默认配置合并，确保有新增的配置项
            for key, value in loaded_config.items():
                if key in self.config:
                    self.config[key] = value
                    
            # 保存回文件，确保新增的配置项也被保存
            self.save_config()
            
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            # 如果加载失败，使用默认配置
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True)
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项并保存"""
        if key in self.config:
            self.config[key] = value
            self.save_config()
            return True
        return False