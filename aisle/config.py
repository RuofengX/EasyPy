import os
import time

# 跨语言兼容性编码

GLOBAL_ENCODING = 'GB2312'

# 日志等级， in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
# Deprecated
LOG_LEVEL = 'INFO'

# 环境变量
# Deprecated
ENVIRON_DICT = os.environ

# 全局日志记录器名称
# Deprecated
GLOBAL_LOGGER_NAME = 'Global'  # 对应了全局日志实例LOG的名称显示名称


# Deprecated
GLOBAL_EXCEPTION_LOGGER_NAME = 'Except'  # 对应了全局异常日志实例LOG的名称显示名称

SPLIT_LINE = """# --------------------------------------------------------"""

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
STRFTIME = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())


# Deprecated
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

