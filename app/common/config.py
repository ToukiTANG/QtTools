from qfluentwidgets import QConfig, ConfigItem, qconfig, Theme


class Config(QConfig):
    pass

# 创建配置实例并使用配置文件来初始化它
cfg = Config()
cfg.themeMode.value = Theme.AUTO