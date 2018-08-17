from . import comm
import threading, time, sys, logging, queue
import socket,json
from threading import Thread

class JsonSocketServer(object):
    backlog = 100

    def __init__(self, host, port, msg_handler):
        self.msg_listeners = []
        self.msg_handler = msg_handler

        self.clients = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.backlog)

        self.client_listener = JsonSocketServerClientListener(self)
        self.client_listener.start()

    def __del__(self):
        self.close()

    def accept(self):
        client, client_addr = self.socket.accept()

        if client_addr in self.clients:
            self.clients[client_addr].close()
            client, client_addr = self.socket.accept()

        self.add_client(client_addr, client)
        logging.info("new connection:", self.clients[client_addr]["conn"], self.clients[client_addr]["address"])
        return self.clients[client_addr]["conn"], self.clients[client_addr]["address"]

    def add_client(self, addr, conn):
        self.clients[addr] = {"conn":conn, "address": addr}

    def remove_client(self, addr):
        del self.clients[addr]


    def boardcast(self, data):
        for k in self.clients:
            comm.send_msg(self.clients[k]["conn"], data)
            #_send(self.clients[k]["client"], data)


    def send(self, client_address, data):
        if client_address not in self.clients:
            raise Exception('Cannot send data, no client is connected')
        #_send(self.clients[client_address], data)
        comm.send_msg(self.clients[client_address]["conn"], data)
        return self


    def close(self):
        for key in self.clients:
            self.clients[key]['conn'].close()
        self.clients = {}

        if self.socket:
            self.socket.close()
            self.socket = None



class JsonSocketServerClientListener(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server


    def run(self):
        while True:
            logging.info('JsonSocketClientListener: waiting for a connection')
            conn, addr = self.server.accept()
            msg_listener = JsonSocketServerMessageListener(self.server, conn, addr)
            self.server.msg_listeners.append(msg_listener)
            msg_listener.start()
            print("new_client")


class JsonSocketServerMessageListener(Thread):
    def __init__(self, server, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.server = server


    def run(self):
        is_running = True

        buf = b""
        while is_running:
            try:
                data = _recvAllMsg(self.conn)
                if data is False:
                    is_running = False
                    print("stop reading")
                else:
                    buf += data

                    while len(buf) > 0:
                        (size, msg, buf) = comm.read_msg(buf)
                        logging.debug("size:%d msg.size:%d msg:|%s| buf:%s|", size,
                                      len(msg), buf, "|")
                        if msg:
                            data = msg.decode("utf-8")
                            data = json.loads(data)
                            self.server.msg_handler(self.addr, data)
                        else:
                            logging.debug("more incoming packet(s) are needed ")
                            break
            except Exception as e:
                print("error:" , sys.exc_info())
                is_running = False
        self.conn.close()
        self.server.remove_client(self.addr)




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
            logging.debug("len %d raw:%s|", len(buf), buf)

            if len(buf) < 4096:
                cont = False
        except ConnectionResetError as e:
            logging.debug("exception from _recvAllMsg %s", sys.exc_info())
            return e
        except:
            print("_recvAllMsg except !", sys.exc_info())
            logging.debug("exception from _recvAllMsg %s", sys.exc_info())
    return allbuf