import logging
import time

class LogMixin():
    """
    日志功能Mixin
    配置了一些简单常用的功能方便使用。
    Properties:
        self.logger: logger实例
    """

    def __init__(self, *keys, **kwargs):

        _name = self.__class__.__name__
        self.logger = logging.getLogger(name=_name)
        self.logger.debug('创建日志功能 > {}'.format(_name))
        
        
        super().__init__(*keys, **kwargs)
        '''提示：
        这里一定要在最后super()，因为有些类会在初始化Mixin之前的父类后直接开始运行，
        例如同时继承LogMixin和StreamRequestHandler的类，传递给ThreadingTCPServer类构造时，会导致Mixin无法正常初始化
        '''
        
    def renameLogger(self, _name):
        '''
        重命名logger
        '''
        self.logger = logging.getLogger(name=_name)
        self.logger.debug('重命名日志功能 > {}'.format(_name))
    
    def __del__(self):
        self.loggerDict.pop(self.__class__.__name__)
        super().__del__()
        
    
    
    
    
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
