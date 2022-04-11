# 一个轻量化的日志模块
import copy
import inspect
import sys
import time
from time import sleep
from rich.console import Console
from multiprocessing import Queue, Process, freeze_support

class AisleLoggerBase():
    def __init__(self, name, level_str: str = None):
        
        self._map = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4
        }
        self._level_str = [
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ]
        self.name = name if name else self.__class__.__name__
        self.format_string = '|{asctime:.19}| [{name}] <{levelname:><9}> {message}'
        
        if level_str is None:
            level_str = 'WARNING'  # 默认为警告
        self.set_level(level_str)

    def set_level(self, level_str: str = None):
        try:
            self._level = self._map[level_str]
        except KeyError:
            raise KeyError(f'无效的日志等级，请使用DEBUG/INFO/WARNN/ERROR/CRITI')

    def get_child(self, suffix: str):
        """
        返回一个子logger
        
        名字为父logger名字+suffix
        日志等级为父logger的日志等级
        """
        new = copy.copy(self)
        new.name = f'{self.name}.{suffix}'
        return new
    
    def getChild(self, suffix: str):
        """Deprecated"""
        return self.get_child(suffix)

    def debug(self, msg: str):
        raise NotImplementedError

    def info(self, msg: str):
        raise NotImplementedError

    def warning(self, msg: str):
        raise NotImplementedError

    def error(self, msg: str):
        raise NotImplementedError

    def critical(self, msg: str):
        raise NotImplementedError

        
class OutputProcess(Process):
    def __init__(self) -> None:
        """单独一个进程来处理打印"""
        self.msgQueue = Queue()
        super().__init__(daemon=False)

    def run(self) -> None:
        console = Console(color_system='auto')  # 线程专用console
        console.log(f'日志进程启动')
        console.log(f'日志进程不会随主进程一同退出，请手动关闭')

        try:
            while 1:
                """循环处理打印队列"""

                while self.msgQueue.qsize() == 0:
                    """如果队列为空，则等待"""
                    sleep(0.01)

                """如果队列不为空，输出队列中的消息"""
                cmd, msg = self.msgQueue.get()
                assert isinstance(msg, str) or (msg is None)  # 控制日志的内容
                assert cmd in [-2, -1, 0, 1, 2, 3, 4]  # 指令

                if cmd >= 0:

                    # 状态机
                    if cmd == 0:
                        console.print(msg, style='white italic')
                    elif cmd == 1:
                        console.print(msg, style='white')
                    elif cmd == 2:
                        console.print(msg, style='yellow')
                    elif cmd == 3:
                        console.print(msg, style='bold red')
                    elif cmd == 4:
                        console.print(msg, style='bold black on red')
                    pass

        except Exception as e:
            console.log(f'日志功能异常 > {type(e)} {e}')
            return

class ProcessLogger(AisleLoggerBase):
    _p = OutputProcess()  # 日志打印进程，可以灵活开关

    @classmethod
    def startLoggerDaemon(cls):
        """开启打印进程

        可重入
        """
        if cls._p.is_alive():
            return

        freeze_support()
        cls._p.start()
        cls._p.msgQueue.put((-1, None))

    def __init__(self, name: str = None, max_workers: int = None):

        super().__init__(name=name)
        self.startLoggerDaemon()

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
        if targetLevel >= self._level:
            msg = self.format_string.format(
                asctime=time.asctime(),
                levelname=self._level_str[targetLevel],
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
        if targetLevel >= self._level:
            self._p.msgQueue.put((targetLevel, msg))


class SyncLogger(AisleLoggerBase):
    """同步日志记录器
    
    一个简单的日志记录器，无状态"""
    style = {
        'fore':
        {   # 前景色
            'black': 30,  # 黑色
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple': 35,  # 紫红色
            'cyan': 36,  # 青蓝色
            'white': 37,  # 白色
        },

        'back':
        {   # 背景
            'black': 40,  # 黑色
            'red': 41,  # 红色
            'green': 42,  # 绿色
            'yellow': 43,  # 黄色
            'blue': 44,  # 蓝色
            'purple': 45,  # 紫红色
            'cyan': 46,  # 青蓝色
            'white': 47,  # 白色
        },

        'mode':
        {   # 显示模式
            'mormal': 0,  # 终端默认设置
            'bold': 1,  # 高亮显示
            'underline': 4,  # 使用下划线
            'blink': 5,  # 闪烁
            'invert': 7,  # 反白显示
            'hide': 8,  # 不可见
        },

        'default':
        {
            'end': 0,
        },
    }

    def __init__(self, name: str = None):
        super().__init__(name=name)

    def set_level(self, level_str: str = None):
        """增加功能：当日志等级为DEBUG时，额外输出调用者信息"""
        if level_str == 'DEBUG':
            self.format_string = '|{asctime:.19}| [{name}@{call}] <{levelname:><9}> {message}'
        return super().set_level(level_str)
    
    def getChild(self, suffix: str):
        return super().get_child(suffix)

    def debug(self, msg: str):
        msg = self.__format(0, msg)
        self.__send(0, msg)

    def info(self, msg: str):
        msg = self.__format(1, msg)
        self.__send(1, msg)

    def warning(self, msg: str):
        msg = self.__format(2, msg)
        self.__send(2, msg)

    def error(self, msg: str):
        msg = self.__format(3, msg)
        self.__send(3, msg)

    def critical(self, msg: str):
        msg = self.__format(4, msg)
        self.__send(4, msg)

    def __format(self, targetLevel: int, msg: str):
        call = ''
        if self._level == 0:
            call = inspect.stack()[2].function
            
        msg = self.format_string.format(
            asctime=time.asctime(),
            levelname=self._level_str[targetLevel],
            name=self.name,
            call=call,
            message=msg
        )
        return msg

    def __send(self, targetLevel: int, msg: str):

        if targetLevel < self._level:
            return
        
        cmd = targetLevel

        # 状态机
        if cmd == 0:
            msg = self.__useStyle(msg, fore='white')
        elif cmd == 1:
            msg = self.__useStyle(msg, fore='green')
        elif cmd == 2:
            msg = self.__useStyle(msg, fore='yellow')
        elif cmd == 3:
            msg = self.__useStyle(msg, fore='red')
        elif cmd == 4:
            msg = self.__useStyle(msg, fore='purple')
        # msg += '\n'
        # sys.stdout.write(msg)
        print(msg, file=sys.__stdout__)
        

    def __useStyle(self, msg: str, mode: str='', fore:str='', back:str=''):
        # mode  = '%s' % self.style['mode'][mode] if mode in self.style['mode'].keys() else ''
        fore  = '%s' % self.style['fore'][fore] if fore in self.style['fore'].keys() else ''
        # back  = '%s' % self.style['back'][back] if back in self.style['back'].keys() else ''
        style = ';'.join([s for s in [mode, fore, back] if s])  # TODO: 将这一部分做到self.__format中
        style = '\033[%sm' % style if style else ''
        end   = '\033[%sm' % self.style['default']['end'] if style else ''
        return '%s%s%s' % (style, msg, end)

if __name__ == '__main__':
    def benchmark(n):
        alogger = SyncLogger()
        alogger.set_level('INFO')  # 会导致两次输出
        start = time.time()
            
        
        if n <= 0:
            end = time.time()
        else:
            for i in range(n):
                alogger.debug('这是一条debug消息')
                alogger.info('这是一条info消息')
                alogger.warning('这是一条警告消息')
                alogger.error('这是一条错误消息')
                alogger.critical('这是一条崩溃消息')
            end = time.time()
            
        return end - start

    # n = 1
    n = 500
    base = benchmark(0)
    result = benchmark(n)
    result -= base
    
    timeAvg = result / n / 5 * 1000
    print(f'每条消息大约阻塞{timeAvg:.3}毫秒')
    print(f'{n*5}条消息共消耗{result:.3}秒')

