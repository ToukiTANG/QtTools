# logger.py
import logging
import sys
from datetime import datetime

# ----------------- 配置日志文件名 -----------------
today = datetime.now().strftime("%Y-%m-%d")
log_file = f"{today}.txt"  # 日志文件后缀为 txt

# ----------------- 配置 logging -----------------
logger = logging.getLogger("ProjectLogger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# 文件输出
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ----------------- print 重定向 -----------------
class LoggerRedirect:
    def write(self, message):
        message = message.strip()
        if message:
            logger.info(message)
    def flush(self):
        pass

sys.stdout = LoggerRedirect()
sys.stderr = LoggerRedirect()

# ----------------- 全局异常捕获 -----------------
def log_uncaught_exceptions(exctype, value, tb):
    logger.critical("未捕获异常:", exc_info=(exctype, value, tb))

sys.excepthook = log_uncaught_exceptions

# ----------------- log() 函数 -----------------
def log(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.info(message)
