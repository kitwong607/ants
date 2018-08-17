from . import comm
import threading, time, sys, logging, queue
import socket,json
from threading import Thread



class JsonSocketClient():
    def __init__(self, host, port, data_handler):
        self.msg_queue = queue.Queue()
        self.host = host
        self.port = port

        self.data_handler = data_handler

        self.reader = None
        self.socket = None
        self.queue_monitor = None
        self.data_handler = data_handler
        self.done = False
        self.connected = False

        self.lock = threading.Lock()

        self.reconnector = JsonSocketClientReconnnector(self)
        self.reconnector.start()


    def connect(self):
        if self.isConnected():
            return

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))


            self.reader = SocketClientReader(self)
            self.reader.start()


            self.queue_monitor = MsgQueueMonitor(self)
            self.queue_monitor.start()

            self.done = False
            self.connected = True

            self.sendMsg({"status":"connect"})
        except socket.error:
            self.connected = False

        print(socket)
        self.socket.settimeout(1)  # non-blocking

    def disconnect(self):
        self.lock.acquire()
        try:
            print("disconnect")
            logging.debug("ants socket disconnecting")
            if self.socket is not None:
                self.reader.is_running = False
                self.queue_monitor.is_running = False

                self.socket.close()
                logging.debug("ants socket disconnected")

                self.done = True
                self.connected = False
        finally:
            self.lock.release()

    def isConnected(self):
        # TODO: also handle when socket gets interrupted/error
        return self.connected

    def sendMsg(self, d):
        if self.socket is None or (not self.isConnected()):
            print("socket is not ready")
            return

        try:
            serialized = json.dumps(d)

        except (TypeError, ValueError) as e:
            raise Exception('You can only send JSON-serializable data')
        msg = comm.make_msg(serialized)
        self.socket.send(msg)


    def recvMsg(self):
        if not self.isConnected():
            logging.debug("recvMsg attempted while not connected, releasing lock")
            return b""
        try:
            buf = _recvAllMsg(self.socket)

        except socket.timeout:
            logging.debug("exception from recvMsg %s", sys.exc_info())
            buf = b""

        except socket.error:
            print("siocket error in recvMsg")
            print(sys.exc_info())
            #self.disconnect()

            #self.connected = False
            logging.debug("exception from recvMsg %s", sys.exc_info())
            buf = b""
        else:
            pass

        return buf


class JsonSocketClientReconnnector(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            isDo = False
            if self.client.socket is None:
                isDo = True
                print("self.client.socket is none")
            elif self.client.isConnected() is False:
                print("self.client.isConnected is False")
                isDo = True

            if isDo:
                print()
                print("Try to connect to json server...")
                time.sleep(3)
                self.client.connect()


class MsgQueueMonitor(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.msg_queue = self.conn.msg_queue
        self.is_running = True

    def run(self):
        self.is_running = True
        try:
            while self.is_running:
                if self.conn.isConnected() and not self.msg_queue.empty():
                    #while not self.conn.done and self.conn.isConnected() and not self.msg_queue.empty():
                    try:
                        try:
                            try:
                                text = self.msg_queue.get(block=True, timeout=0.2)
                            except:
                                logging.debug("exception from MsgQueueMonitor %s", sys.exc_info())

                            if len(text) > 4096:
                                self.conn.disconnect()
                                break
                            else:
                                data = text.decode("utf-8")
                                data = json.loads(data)
                                self.conn.data_handler(data)

                        except queue.Empty:
                            logging.debug("queue.get: empty")
                        except error:
                            logging.debug("exception from MsgQueueMonitor %s", sys.exc_info())


                            # self.decoder.interpret(fields)
                    except (KeyboardInterrupt, SystemExit):
                        logging.info("detected KeyboardInterrupt, SystemExit")
                        self.keyboardInterrupt()
                        self.keyboardInterruptHard()

                    logging.debug("conn:%d queue.sz:%d",
                                  self.conn.isConnected(),
                                  self.msg_queue.qsize())
        except:
            print("except !")
            logging.debug("exception from MsgQueueMonitor %s", sys.exc_info())

        finally:
            print("final !")
            print("MsgQueueMonitor thread finished")
            self.conn.disconnect()

class SocketClientReader(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.msg_queue = self.conn.msg_queue
        self.is_running = True

    def run(self):
        self.is_running = True
        buf = b""
        while self.is_running:
            if self.conn.isConnected():
                data = self.conn.recvMsg()

                if data is False:
                    self.is_running = False
                    self.conn.disconnect()
                else:
                    logging.debug("reader loop, recvd size %d", len(data))
                    buf += data

                    while len(buf) > 0:
                        (size, msg, buf) = comm.read_msg(buf)
                        # logging.debug("resp %s", buf.decode('ascii'))
                        logging.debug("size:%d msg.size:%d msg:|%s| buf:%s|", size,
                                      len(msg), buf, "|")

                        if msg:
                            self.msg_queue.put(msg)
                        else:
                            logging.debug("more incoming packet(s) are needed ")
                            break

        print("SocketClientReader thread finished")
        logging.debug("SocketClientReader thread finished")












## helper functions ##
'''
def _send(socket, data):
    try:
        serialized = json.dumps(data)

    except (TypeError, ValueError) as e:
        raise Exception('You can only send JSON-serializable data')
    msg = comm.make_msg(serialized)
    socket.send(msg)
'''


def _recvAllMsg(conn):
    cont = True
    allbuf = b""

    while cont:
        try:
            buf = conn.recv(4096)
            allbuf += buf
            print(buf)
            logging.debug("len %d raw:%s|", len(buf), buf)
            if len(buf) < 4096:
                cont = False
                print("message complete")
        except ConnectionResetError as e:
            logging.debug("exception from _recvAllMsg %s", sys.exc_info())
            return False
        '''
        except:
            print("exception _recvAllMsg", sys.exc_info())
            logging.debug("exception from _recvAllMsg %s", sys.exc_info())
        '''
    return allbuf