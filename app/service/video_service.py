import os
import re
import subprocess
import sys

from PyQt5.QtCore import QThread, pyqtSignal


def get_ffmpeg_path(exe: str):
    """
    返回打包后或开发环境下 ffmpeg.exe 的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # 打包后，base_path 指向可执行文件所在目录
        base_path = os.path.dirname(sys.executable)
    else:
        # 开发环境，base_path 指向项目根目录
        # video.py 在 app/service 下，tools 在根目录
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, 'tools', exe)


FFMPEG_PATH = get_ffmpeg_path('ffmpeg.exe')
# FFPLAY_PATH = get_ffmpeg_path('ffplay.exe')   #暂时不用播放相关的功能
FFPROBE_PATH = get_ffmpeg_path('ffprobe.exe')


class VideoFormatConverter(QThread):
    # 用于更新进度条
    progressChanged = pyqtSignal(int)
    # 视频转换完成信号
    finished = pyqtSignal()

    def __init__(self, input_file: str, outputFile: str, preset='veryfast', parent=None):
        super().__init__(parent)
        self.ffmpegCommand = FFmpegCommand()
        self.input_file = input_file
        self.outputFile = outputFile
        self.preset = preset
        self.process = None

    def run(self):
        video_duration = get_video_duration(self.input_file)
        self.process = self.ffmpegCommand.execute(self.input_file, self.outputFile, preset=self.preset)
        while True:
            stderr_line = self.process.stderr.readline()
            if stderr_line == '' and self.process.poll() is not None:
                break  # 进程结束，退出循环

            if stderr_line:
                match = re.search(r"time=(\d+:\d+:\d+\.\d+)", stderr_line)
                if match:
                    time_str = match.group(1)
                    time_parts = time_str.split(":")
                    seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + float(time_parts[2])
                    progress = min(100, (seconds / video_duration) * 100)  # 计算进度
                    self.progressChanged.emit(round(progress))
        self.process.wait()  # 等待 ffmpeg 完成
        self.finished.emit()

    def terminate(self):
        self.process.terminate()
        super().terminate()


def get_video_duration(input_file):
    # 使用 ffprobe 获取视频时长（秒数）
    command = [FFPROBE_PATH, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())


class FFmpegCommand:
    def __init__(self, ):
        self.command = [FFMPEG_PATH]  # 基础命令

    def add_input(self, input_file: str):
        self.command.extend(["-i", f"{input_file}"])  # 添加输入文件

    def add_output(self, output_file: str):
        self.command.append(f"{output_file}")  # 添加输出文件

    def add_codec(self, codec: str):
        self.command.extend(["-c:v", codec])  # 添加视频编解码器

    def add_audio_codec(self, codec: str):
        self.command.extend(["-c:a", codec])  # 添加音频编解码器

    def add_option(self, option: str, value: str):
        self.command.extend([option, value])  # 添加自定义选项

    def add_preset(self, preset: str):
        self.command.extend(["-preset", preset])  # 添加编码预设

    def add_crf(self, crf: int):
        self.command.extend(["-crf", str(crf)])  # 添加质量设置

    def add_time_limit(self, time_limit: str):
        self.command.extend(["-t", time_limit])  # 添加转换时间限制

    def add_overwrite_option(self):
        # 强制覆盖输出文件
        self.command.append("-y")

    def execute(self, input_file: str, output_file: str, videoCodec='libx264', preset='veryfast', audioCodec=None, quality=28, timeLimit=None):
        self.add_input(input_file)
        self.add_codec(videoCodec)
        if audioCodec:
            self.add_audio_codec(audioCodec)
        self.add_preset(preset)
        self.add_crf(quality)
        self.add_output(output_file)
        if timeLimit:
            self.add_time_limit(timeLimit)
        self.add_overwrite_option()

        print(f'ffmpeg command: {self.command}')

        return subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == '__main__':
    # ffmpeg = FFmpegCommand()
    # ffmpeg.execute(input_file=r"C:\Users\Touki\Videos\2025-08-30 10-11-39.mkv", output_file=r"C:\Users\Touki\Videos\test.mp4")
    # let = get_video_duration(r"C:\Users\Touki\Videos\2025-08-30 10-11-39.mkv")
    # print(let)
    print(int(99.55271565495207))
