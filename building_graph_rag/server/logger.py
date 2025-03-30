# coding: utf-8
import sys
import yaml
from loguru import logger
from config import server_config

log_path = server_config.log_path
log_prefix = server_config.log_prefix
log_rotation = server_config.log_rotation
log_retention = server_config.log_retention
log_encoding = server_config.log_encoding
log_backtrace = server_config.log_backtrace
log_diagnose = server_config.log_diagnose

# 格式里面添加了process和thread记录，方便查看多进程和多线程程序
format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> " \
        "| <magenta>{process}</magenta>:<yellow>{thread}</yellow> " \
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>"

# 这里采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富
# 最高级日志更少更关键
# debug
logger.add(log_path + log_prefix + "debug.log", level="DEBUG", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=False, rotation=log_rotation, retention=log_retention, encoding=log_encoding,
           filter=lambda record: record["level"].no >= logger.level("DEBUG").no)

# info
logger.add(log_path + log_prefix + "info.log", level="INFO", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=False, rotation=log_rotation, retention=log_retention, encoding=log_encoding,
           filter=lambda record: record["level"].no >= logger.level("INFO").no)

# warning
logger.add(log_path + log_prefix + "warning.log", level="WARNING", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=False, rotation=log_rotation, retention=log_retention, encoding=log_encoding,
           filter=lambda record: record["level"].no >= logger.level("WARNING").no)

# error
logger.add(log_path + log_prefix + "error.log", level="ERROR", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=False, rotation=log_rotation, retention=log_retention, encoding=log_encoding,
           filter=lambda record: record["level"].no >= logger.level("ERROR").no)

# critical
logger.add(log_path + log_prefix + "critical.log", level="CRITICAL", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=False, rotation=log_rotation, retention=log_retention, encoding=log_encoding,
           filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)

logger.add(sys.stderr, level="CRITICAL", backtrace=log_backtrace, diagnose=log_diagnose,
           format=format, colorize=True,
           filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)