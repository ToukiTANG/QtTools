import sys
import os

# 程序版本号
VERSION = "0.0.1"

if sys.platform == "win32":
    # Nuitka 打包参数
    args = [
        "nuitka",
        "--standalone",  # 独立 exe，包含所有依赖
        # "--onefile",    # 单个exe
        "--windows-console-mode=disable",  # 去掉黑框控制台
        "--plugin-enable=pyqt5",  # 启用 PyQt5 插件
        "--include-data-file=tools/*.exe=tools/",
        "--assume-yes-for-downloads",  # 自动同意下载依赖
        "--mingw64",  # 使用 MinGW 编译
        "--show-memory",  # 显示编译内存信息
        "--show-progress",  # 显示进度
        "--windows-icon-from-ico=app/resource/icons/China_Railways.ico",  # 图标
        f"--windows-file-version={VERSION}",
        f"--windows-product-version={VERSION}",
        '--windows-file-description="Qt-Tools"',
        "--output-dir=dist",  # 输出目录
        "Qt-Tools.py",  # 入口脚本
    ]
else:
    args = [
        'pyinstaller',
        '-w',
        'Qt-Tools.py',
    ]

# 拼接命令执行
os.system(" ".join(args))
