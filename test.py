from aisle import LOG, LogMixin, CliHelper
import time

@CliHelper
def test():
    '''测试函数'''
    time.sleep(1)

class TestCls(LogMixin):
    def __init__(self):
        super().__init__()
        self.logger.set_level('DEBUG')
        self.logger.critical('测试类')
        
        
def cls_test():
    c = TestCls()
    c.logger.info(f'LogMixin.logger: {c.logger}')
    
def benchmark(n):
    o = LogMixin()
    logger = o.logger
    past = time.time()
    for i in range(n):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warn')
        logger.error('error')
        logger.critical('critical')
    timeAvg = (time.time() - past) / n / 5 * 1000
    logger.warning(f'每条消息耗时{timeAvg:.2}毫秒')
    
if __name__ == '__main__':
    test()
    cls_test()
    LOG.critical('全局测试')
    # benchmark(10)
    
    
    