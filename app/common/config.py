import enum
import os

from qfluentwidgets import QConfig, Theme


class SupportVideoFormat(enum.Enum):
    MP4 = 'mp4'
    MOV = 'mov'
    AVI = 'avi'
    MKV = 'mkv'

    @classmethod
    def values(cls):
        """返回所有枚举值列表"""
        return [f.value for f in cls]

    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """判断文件是否是支持的视频格式"""
        ext = os.path.splitext(file_path)[1].lower().lstrip(".")  # 取后缀名
        return ext in cls.values()


class VideoConversionSpeed(enum.Enum):
    ULTRAFAST = ('快', '快速的转换速度，输出文件较大，质量较差')
    MEDIUM = ('适中', '普通转换，输出文件大小与质量适中')
    VERYSLOW = ('慢', '较慢的转换速度，输出文件较小，质量较高')

    def __init__(self, label, description):
        self.label = label  # 显示在 ComboBox 中的标签
        self.description = description  # 对应的描述

    @classmethod
    def labels(cls):
        return [f.label for f in cls]


class Config(QConfig):
    pass


# 创建配置实例并使用配置文件来初始化它
cfg = Config()
cfg.themeMode.value = Theme.AUTO
