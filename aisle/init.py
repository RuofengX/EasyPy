import logging
import logging.config
import sys
from .config import GLOBAL_LOGGER_NAME, GLOBAL_EXCEPTION_LOGGER_NAME, LOG_LEVEL
from .utils import SyncLogger

# Depricated
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

LOG = SyncLogger(GLOBAL_LOGGER_NAME)
LOG.set_level('INFO')

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Credits

# LOG.debug(
#     f'多彩日志，来自Sam Clements的colorlog, https://github.com/borntyping/python-colorlog')

# # 手动加载Colorlog，避免IDE报错
# _COLORLOG_IS_NECESSARY = colorlog

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''添加全局异常日志

避免使用logging.debug()时创建新的handler混淆日志

'''

EXCP_LOG = SyncLogger(GLOBAL_EXCEPTION_LOGGER_NAME)
EXCP_LOG.set_level('INFO')


def _exception_handler(exception_type, exception_value, traceback):
    '''All trace are belong to this!'''

    EXCP_LOG.critical(
        f"检测到程序异常！Error catched!{exception_type.__name__}({exception_value})")
    sys.exit(1)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def catch_exception():
    '''
    将异常处理函数添加到sys.excepthook
    '''
    sys.excepthook = _exception_handler
    
if LOG_LEVEL != "DEBUG":
    catch_exception()
