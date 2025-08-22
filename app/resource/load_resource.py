import os
import subprocess
import shutil

"""
Author:      Touki
Date:        2025/8/22 15:58
Description: 这个脚本用于添加resource资源后进行编译生成resources.qrc及resources_rc.py文件
             实现了：
             1、自动扫描resource文件下的VALID_EXTENSIONS（下方定义）允许的资源文件
             2、使用文件所在的文件夹为prefix分组前缀并使用文件名（带扩展名）为alias别名
"""

# 可以在这里添加需要扫描的文件夹
RESOURCE_DIRS = ["images", "icons"]
QRC_FILE = "resources.qrc"
RC_PY_FILE = "resources_rc.py"
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".ico", ".bmp"}


def generate_qrc():
    qrc_content = ["<RCC>"]

    for folder in RESOURCE_DIRS:
        if not os.path.exists(folder):
            continue

        qrc_content.append(f'    <qresource prefix="/{folder}">')

        for root, _, filenames in os.walk(folder):
            for name in filenames:
                ext = os.path.splitext(name)[1].lower()
                if ext in VALID_EXTENSIONS:
                    rel_path = os.path.relpath(os.path.join(root, name), ".")
                    rel_path = rel_path.replace("\\", "/")
                    # 文件名作为 alias
                    alias = os.path.basename(rel_path)
                    qrc_content.append(f'        <file alias="{alias}">{rel_path}</file>')

        qrc_content.append("    </qresource>")

    qrc_content.append("</RCC>")

    with open(QRC_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(qrc_content))

    print(f"✅ 已生成 {QRC_FILE}")
    return True


def compile_qrc():
    if shutil.which("uv"):  # uv 环境
        try:
            subprocess.check_call(["uv", "run", "pyrcc5", QRC_FILE, "-o", RC_PY_FILE])
            print(f"✅ 已编译 {QRC_FILE} → {RC_PY_FILE} (PyQt5)")
            return
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call(["uv", "run", "pyside6-rcc", QRC_FILE, "-o", RC_PY_FILE])
                print(f"✅ 已编译 {QRC_FILE} → {RC_PY_FILE} (PySide6)")
                return
            except subprocess.CalledProcessError:
                pass

    print("❌ 没找到 pyrcc5 或 pyside6-rcc，请确认在 uv 环境里安装了 PyQt5 或 PySide6")


if __name__ == "__main__":
    if generate_qrc():
        compile_qrc()
