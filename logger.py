from .session import SessionStaticVariable
from . import utilities
import datetime
from threading import Thread
from concurrent.futures import Future

def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)

def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future
    return wrapper


class AntLogger(object):
# region Function: Log
    def __init__(self, logFolder):
        utilities.createFolder(SessionStaticVariable.logDirectory + logFolder)
        self.logFilePath = datetime.datetime.now().strftime(
            SessionStaticVariable.logDirectory + logFolder + "/consolgLog" + "_%Y%m%d_%H%M%S.log")
        with open(self.logFilePath, 'a', newline='') as f:
            f.close()

        self.Log("Log file created:", self.logFilePath)

    def Log(self, *args):
        msg = (" ".join(map(str, args)))
        self.LogToFile(msg)
        #threading._start_new_thread(self.LogToFile, (msg,))

    @threaded
    def LogToFile(self, _message):
        new_message = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]") + " " + _message
        print(new_message)

        with open(self.logFilePath, 'a', newline='') as f:
            f.write(new_message + "\r")
            f.close()
# endregion
