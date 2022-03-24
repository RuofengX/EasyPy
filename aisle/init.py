from distutils.debug import DEBUG
import logging
import logging.config
import colorlog
import sys
import os
import time
from aisle.config import GLOBAL_LOGGER_NAME, GLOBAL_EXCEPTION_LOGGER_NAME, LOG_LEVEL


'''
日志格式化配置
以字典的形式配置logging.getLogger()默认返回的日志记录器，以此设置了全局格式。相关文档👇
https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-logging-config-dictconfig
https://pypi.org/project/colorlog/
https://docs.python.org/zh-cn/3.7/library/logging.config.html#configuration-dictionary-schema
'''
LOG_DICT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'aisle': {
            '()': 'colorlog.ColoredFormatter',
            'format': '|{asctime:.19}| {log_color}<{levelname:><9} [{name}|{funcName}] {message}',
            'style': '{'
        }
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'formatter': 'aisle',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        # 有bug，不能输出到文件
        # 'file': {
        #     'level': 'DEBUG',
        #     'class' : 'logging.handlers.RotatingFileHandler',
        #     'formatter': 'aisle',
        #     'filename': f'{STRFTIME}.log',
        #     'maxBytes': 1024,
        #     'backupCount': 3
        #     }
    },
    'loggers': {
        # 当``logging.getLogger()``请求一个名字为空的logger时返回的配置，这也是大多数情况
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        # 当``logging.getLogger('uvicorn')``请求一个名字为uvicorn的logger时返回的配置
        # 相当于uvicorn的配置
        'uvicorn': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        # 当``logging.getLogger('PyInstaller')``请求一个名字为PyInstaller的logger时返回的配置
        # 相当于PyInstaller的配置
        'PyInstaller': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        }

    }
}

logging.config.dictConfig(LOG_DICT_CONFIG)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
配置全局logger
添加全局LOG，避免使用logging.debug()时创建新的handler混淆日志
'''

LOG = logging.getLogger(GLOBAL_LOGGER_NAME)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Credits

LOG.debug(
    f'多彩日志，来自Sam Clements的colorlog, https://github.com/borntyping/python-colorlog')

# 手动加载Colorlog，避免IDE报错
_COLORLOG_IS_NECESSARY = colorlog

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''添加全局异常日志

避免使用logging.debug()时创建新的handler混淆日志

'''

EXCP_LOG = logging.getLogger(GLOBAL_EXCEPTION_LOGGER_NAME)
EXCP_LOG.setLevel(LOG_LEVEL)


def _exception_handler(exception_type, exception_value, traceback):
    '''All trace are belong to this!'''

    EXCP_LOG.error(
        f"检测到异常！{exception_type.__name__}({exception_value})")
    sys.exit(1)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if LOG_LEVEL != "DEBUG":
    sys.excepthook = _exception_handler


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 关于DEBUG的警告
if LOG_LEVEL == "DEBUG":
    LOG.warning('警告！您已开启DEBUG模式，日志内容可能存在换行，请手工查阅需要的信息。')
