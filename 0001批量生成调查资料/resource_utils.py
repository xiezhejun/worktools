#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
资源路径管理工具
处理打包前后的路径问题
支持开发环境和PyInstaller打包环境
"""

import os
import sys
from pathlib import Path
from typing import Optional


class ResourcePaths:
    """资源路径管理类"""

    def __init__(self):
        """初始化路径管理器"""
        self._base_path: Optional[Path] = None
        self._is_frozen = getattr(sys, 'frozen', False)

        if self._is_frozen:
            if hasattr(sys, '_MEIPASS'):
                self._base_path = Path(sys._MEIPASS)
            else:
                self._base_path = Path(sys.executable).parent
        else:
            self._base_path = Path(__file__).parent.absolute()

    @property
    def base_path(self) -> Path:
        """获取基础路径"""
        return self._base_path

    @property
    def is_frozen(self) -> bool:
        """是否为打包状态"""
        return self._is_frozen

    def get_resource_path(self, relative_path: str) -> Path:
        """
        获取资源文件的绝对路径
        
        Args:
            relative_path: 相对于基础路径的相对路径
            
        Returns:
            资源文件的绝对路径
        """
        return self._base_path / relative_path

    def get_data_path(self, relative_path: str = "") -> Path:
        """
        获取数据文件的绝对路径
        
        Args:
            relative_path: 相对于数据目录的相对路径
            
        Returns:
            数据文件的绝对路径
        """
        if self._is_frozen:
            data_dir = self._base_path / "data"
        else:
            data_dir = self._base_path / "示例shp"

        if relative_path:
            return data_dir / relative_path
        return data_dir

    def get_output_path(self, relative_path: str = "") -> Path:
        """
        获取输出目录的绝对路径
        
        在开发环境中使用项目目录下的output文件夹
        在打包环境中使用用户文档目录下的output文件夹
        
        Args:
            relative_path: 相对于输出目录的相对路径
            
        Returns:
            输出目录的绝对路径
        """
        if self._is_frozen:
            import os
            home = Path(os.path.expanduser("~"))
            output_dir = home / "Documents" / "SurveyGenerator" / "output"
        else:
            output_dir = self._base_path / "output"

        output_dir.mkdir(parents=True, exist_ok=True)

        if relative_path:
            return output_dir / relative_path
        return output_dir

    def get_log_path(self, filename: str = "app.log") -> Path:
        """
        获取日志文件的绝对路径
        
        Args:
            filename: 日志文件名
            
        Returns:
            日志文件的绝对路径
        """
        if self._is_frozen:
            import os
            home = Path(os.path.expanduser("~"))
            log_dir = home / "Documents" / "SurveyGenerator" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            return log_dir / filename
        else:
            return self._base_path / filename

    def get_temp_path(self, filename: str = "") -> Path:
        """
        获取临时文件的绝对路径
        
        Args:
            filename: 临时文件名
            
        Returns:
            临时文件的绝对路径
        """
        if self._is_frozen:
            import tempfile
            temp_dir = Path(tempfile.gettempdir()) / "SurveyGenerator"
            temp_dir.mkdir(exist_ok=True)
            if filename:
                return temp_dir / filename
            return temp_dir
        else:
            temp_dir = self._base_path / "temp"
            temp_dir.mkdir(exist_ok=True)
            if filename:
                return temp_dir / filename
            return temp_dir

    def ensure_directory(self, path: Path) -> Path:
        """
        确保目录存在，不存在则创建
        
        Args:
            path: 目录路径
            
        Returns:
            目录路径
        """
        path.mkdir(parents=True, exist_ok=True)
        return path


_global_resource_paths: Optional[ResourcePaths] = None


def get_resource_paths() -> ResourcePaths:
    """
    获取全局资源路径管理器实例
    
    Returns:
        ResourcePaths实例
    """
    global _global_resource_paths
    if _global_resource_paths is None:
        _global_resource_paths = ResourcePaths()
    return _global_resource_paths


def get_resource_path(relative_path: str) -> Path:
    """
    快捷方法：获取资源文件路径
    
    Args:
        relative_path: 相对路径
        
    Returns:
        绝对路径
    """
    return get_resource_paths().get_resource_path(relative_path)


def get_data_path(relative_path: str = "") -> Path:
    """
    快捷方法：获取数据文件路径
    
    Args:
        relative_path: 相对路径
        
    Returns:
        绝对路径
    """
    return get_resource_paths().get_data_path(relative_path)


def get_output_path(relative_path: str = "") -> Path:
    """
    快捷方法：获取输出目录路径
    
    Args:
        relative_path: 相对路径
        
    Returns:
        绝对路径
    """
    return get_resource_paths().get_output_path(relative_path)


def get_log_path(filename: str = "app.log") -> Path:
    """
    快捷方法：获取日志文件路径
    
    Args:
        filename: 日志文件名
        
    Returns:
        绝对路径
    """
    return get_resource_paths().get_log_path(filename)


if __name__ == "__main__":
    paths = get_resource_paths()
    print(f"Base path: {paths.base_path}")
    print(f"Is frozen: {paths.is_frozen}")
    print(f"Resource path: {paths.get_resource_path('test.txt')}")
    print(f"Data path: {paths.get_data_path()}")
    print(f"Output path: {paths.get_output_path()}")
    print(f"Log path: {paths.get_log_path()}")
