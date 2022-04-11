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
    o = LogMixin()
    logger = o.logger
    past = time.time()
    n = 100
    for i in range(n):
        logger.info('debug')
        logger.info('info')
        logger.warning('warn')
        logger.error('error')
        logger.critical('critical')
    timeAvg = (time.time() - past) / n / 5 * 1000
    logger.warning(f'每条消息耗时{timeAvg:.2}毫秒')
    
    
    