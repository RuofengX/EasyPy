from aisle import LOG, LogMixin, CliHelper
import time

@CliHelper
def test():
    '''测试函数'''
    time.sleep(1)

@CliHelper
def debugTest():
    '''专门用来测试debug的函数'''
    raise IOError('测试异常')

class TestCls(LogMixin):
    def __init__(self):
        super().__init__()
        self.logger.critical('测试类')
        
if __name__ == '__main__':
    LOG.error('测试错误')
    test()
    TestCls()
    debugTest()
    