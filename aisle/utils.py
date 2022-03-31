import logging
import time

class LogMixin(object):
    """
    日志功能Mixin
    配置了一些简单常用的功能方便使用。
    Properties:
        self.logger: logger实例
    """
    def __init__(self, *keys, **kwargs):
        super().__init__(*keys, **kwargs)
        
        _name = self.__class__.__name__
        self.logger = logging.getLogger(name=_name)
        self.logger.debug('创建日志功能 > {}'.format(_name))

    def renameLogger(self, _name):
        '''
        重命名logger
        '''
        self.logger = logging.getLogger(name=_name)
        self.logger.debug('重命名日志功能 > {}'.format(_name))

class CliHelper(LogMixin):
    '''一个装饰器，给函数添加Log输出，并快速Debug'''
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.renameLogger(self.func.__name__)
        

    def __call__(self, *args, **kwargs):
        try:
            
            self.logger.info(f'运行 > {self.func.__name__}')
            self.logger.info(f'# > {self.func.__doc__}')
            startTime = time.time()
            rtn = self.func(*args, **kwargs)
            endTime = time.time()
            self.logger.info(f'完成 > 用时{endTime - startTime}秒')
            
            return rtn
        
        except Exception as e:
            self.logger.error(f'{type(e).__name__}: {e}')
            self.logger.error(f'进入pdb模式，将会重新抛出异常...')
            import pdb
            pdb.set_trace()
            raise e
