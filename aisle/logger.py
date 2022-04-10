# 一个轻量化的日志模块
import time
from time import sleep
from typing import *
from rich.console import Console
from multiprocessing import Queue, Process, freeze_support
from concurrent.futures import ProcessPoolExecutor


class AisleLoggerBase():
    def __init__(self):
        self._map = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNNING': 2,
            'ERROR': 3,
            'CRITICAL': 4
        }
        self._levelStr = [
            'DEBUG',
            'INFO',
            'WARNNING',
            'ERROR',
            'CRITICAL'
        ]




class Logger(AisleLoggerBase):
    _msgQueue = Queue()
    _daemonStarted = False
    
    @staticmethod
    def outputProcess(msgQueue: Queue):
        """单独一个进程来处理打印"""
        console = Console()
        console.log(f'日志功能启动')
        try:
            while 1:
                while msgQueue.qsize() == 0:
                    sleep(0.01)
                """循环处理打印队列"""
                msg = msgQueue.get()
                
                assert isinstance(msg, str) or (msg is None)
                
                if msg is None:
                    console.log(f'关闭日志功能')
                    break
                else:
                    console.print(msg)
        except KeyboardInterrupt:
            console.log(f'关闭日志功能')
            return
                
    @classmethod
    def startLoggerDaemon(cls):
        """开启打印进程
        
        可重入
        """
        if cls._daemonStarted:
            return
        # p = ProcessPoolExecutor(1)
        # p.submit(cls.outputProcess, (cls._msgQueue))
        freeze_support()
        p = Process(target=cls.outputProcess, args=(cls._msgQueue,))
        p.start()
        cls._daemonStarted = True
        
    
        
    

    def __init__(self, name: str = None, max_workers: int = None):
        self.name = name if name else self.__class__.__name__
        self.formatString = '|{asctime:.19}| <{levelname:><9} [{name}] {message}'
        
        self._level = 0
        super().__init__()
        self.startLoggerDaemon()
        
        

    def setLevel(self, levelStr: str = None):
        try:
            self.level = self._map[levelStr]
        except KeyError:
            raise KeyError(f'无效的日志等级，请使用DEBUG/INFO/WARNN/ERROR/CRITI')

    def getChild(self, suffix: str):
        return Logger(f'{self.name}.{suffix}')

    def debug(self, msg: str):
        msg = self.__formater(0, msg)
        self.__send(0, msg)
    
    def info(self, msg: str):
        msg = self.__formater(1, msg)
        self.__send(1, msg)
    
    def warning(self, msg: str):
        msg = self.__formater(2, msg)
        self.__send(2, msg)
        
    def error(self, msg: str):
        msg = self.__formater(3, msg)
        self.__send(3, msg)
    
    def critical(self, msg: str):
        msg = self.__formater(4, msg)
        self.__send(4, msg)
    
    def __formater(self, targetLevel: int, msg: str):
        if msg is None:
            msg = 'None'
        if targetLevel >= self.level:
            msg = self.formatString.format(
                asctime=time.asctime(),
                levelname=self._levelStr[targetLevel],
                name=self.name,
                message=msg
            )
            return msg
        else:
            return
        
    def __send(self, targetLevel: int, msg: str):
        """发送到等待打印队列"""
        if msg is None:
            return
        if targetLevel >= self.level:
            self._msgQueue.put(msg)
        

            
            
if __name__ == '__main__':
    logger = Logger()
    logger.setLevel('DEBUG')
    past = time.time()
    n = 100
    for i in range(n):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warn')
        logger.error('error')
        logger.critical('critical')
    timeAvg = (time.time() - past) / n / 5 * 1000
    logger.warning(f'每条消息耗时{timeAvg}毫秒')
    
    