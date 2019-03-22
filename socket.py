import socket, traceback
import struct
import threading
import queue
import sys, json, time, os, datetime
from .session import SessionStaticVariable

TYPE_ALL = "ALL"
TYPE_UI = "UI"
TYPE_STRATEGY = "STRATEGY"

EOL = "[ANT_END]"
STATUS_FAIL = "FAIL"
STATUS_FAIL = "SUCCESS"

ACTION_SET_TYPE = "SET_TYPE"
ACTION_PLACE_ORDER = "PLACE_ORDER"
GET_GATEWAY_STATUS = "GET_GATEWAY_STATUS"
GET_ACCOUNT_INFO = "GET_ACCOUNT_INFO"


GATEWAY_STATUS_RESPONSE = "GATEWAY_STATUS_RESPONSE"
ACCOUNT_INFO_RESPONSE = "ACCOUNT_INFO_RESPONSE"

CONNECTED_TO_SERVER_EVENT = "CONNECTED_TO_SERVER_EVENT"
DISCONNECT_WITH_SERVER_EVENT = "DISCONNECT_WITH_SERVER_EVENT"
MARKET_CLOSE_EVENT = "MARKET_CLOSE_EVENT"

IB_START_EVENT = "IB_START_EVENT"
IB_ERROR_EVENT = "IB_ERROR_EVENT"
WIN_ERROR_EVENT = "WIN_ERROR_EVENT"
OHLC_EVENT = "OHLC_EVENT"
TICK_EVENT = "TICK_EVENT"
TICK_BY_TICK_BID_ASK_EVENT = "TICK_BY_TICK_BID_ASK_EVENT"

OPEN_ORDER_EVENT = "OPEN_ORDER_EVENT"
OPEN_ORDER_END_EVENT = "OPEN_ORDER_END_EVENT"
ORDER_UPDATE_EVENT = "ORDER_UPDATE_EVENT"
POSITION_EVENT = "POSITION_EVENT"
POSITION_MULTI_EVENT = "POSITION_MULTI_EVENT"
POSITION_END_EVENT = "POSITION_END_EVENT"
POSITION_MULTI_END_EVENT = "POSITION_MULTI_END_EVENT"


PORTFOLIO_UPDATE_EVENT = "PORTFOLIO_UPDATE_EVENT"
MANAGED_ACCOUNTS_EVENT = "MANAGED_ACCOUNTS_EVENT"
MANAGED_SUMMARY_EVENT = "MANAGED_SUMMARY_EVENT"
MANAGED_SUMMARY_END_EVENT = "MANAGED_SUMMARY_END_EVENT"

GET_IB_GATEWAY_STATUS_RESPONSE = "GET_IB_GATEWAY_STATUS_RESPONSE"
GET_ACCOUNT_INFO_RESPONSE = "GET_ACCOUNT_INFO_RESPONSE"

CONNECT_TO_GATEWAY_RESPONSE = "CONNECT_TO_GATEWAY_RESPONSE"
DISCONNECT_TO_GATEWAY_RESPONSE = "DISCONNECT_TO_GATEWAY_RESPONSE"
SUBSCRIBE_MKT_DATA_RESPONSE = "SUBSCRIBE_MKT_DATA_RESPONSE"
PLACE_ORDER_RESPONSE = "PLACE_ORDER_RESPONSE"

STRATEGY_EVENT = [PLACE_ORDER_RESPONSE, OPEN_ORDER_END_EVENT, OPEN_ORDER_EVENT, ORDER_UPDATE_EVENT,
                  OHLC_EVENT, TICK_BY_TICK_BID_ASK_EVENT]

UI_EVENT = [IB_START_EVENT, IB_ERROR_EVENT, WIN_ERROR_EVENT, TICK_BY_TICK_BID_ASK_EVENT,
            OPEN_ORDER_EVENT, OPEN_ORDER_END_EVENT, ORDER_UPDATE_EVENT, POSITION_END_EVENT,
            POSITION_MULTI_END_EVENT, ACCOUNT_INFO_RESPONSE, GATEWAY_STATUS_RESPONSE,
            CONNECT_TO_GATEWAY_RESPONSE, DISCONNECT_TO_GATEWAY_RESPONSE,
            SUBSCRIBE_MKT_DATA_RESPONSE, PLACE_ORDER_RESPONSE]

class ThreadedTimer(threading.Thread):
    def __init__(self, duration, functionToCall):
        super(ThreadedTimer, self).__init__()
        self.isStart = True
        self.duration = duration
        self.functionToCall = functionToCall


    def stop(self):
        self.isStart = False


    def run(self):
        while self.isStart:
            self.functionToCall()
            time.sleep(self.duration)


class ProxySocketClientThread(threading.Thread):
    def __init__(self, host, port, messageHandler, type, sid=-1):
        super(ProxySocketClientThread, self).__init__()
        self.maxBufferSize = 2000
        self.host = host
        self.port = port
        self.messageHandler = messageHandler

        self.lastMessage = ""
        self.type = type
        self.sid = sid

        self.logDirectory = SessionStaticVariable.logDirectory + "clientSocket/"
        if not os.path.exists(self.logDirectory):
            os.mkdir(self.logDirectory)

        self.logDirectory = self.logDirectory + self.type + "/"
        if not os.path.exists(self.logDirectory):
            os.mkdir(self.logDirectory)

        self.logDirectory = self.logDirectory + str(sid) + "/"
        if not os.path.exists(self.logDirectory):
            os.mkdir(self.logDirectory)

        self.logFile = "clientSocket_" + str(sid) + datetime.datetime.now().strftime("_%Y%m%d_%H%M%S") +".log"

        self.isConnected = False
        self.isLongMessage = False

        self.connectTimer = ThreadedTimer(2, self.Connect)
        self.connectTimer.start()
        #self.Connect()

    def Log(*args):
        msg = (" ".join(map(str, args)))
        threading._start_new_thread(LogToFile, (msg,))

    def LogToFile(_message):
        global logFile
        newMessage = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") + " " + _message
        print(newMessage)

        with open(self.logFile, 'a', newline='') as f:
            f.write(newMessage + "\n\r")
            f.close()

    def Connect(self):
        if self.isConnected is True: return
        print("Try to connect...")
        try:
            self.proxyClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.proxyClient.connect((self.host, self.port))
        except:
            traceback.print_exc()
            self.isConnected = False
            return
        print("Connected")
        self.isConnected = True

        if self.type == TYPE_STRATEGY:
            self.SendMessage(ACTION_SET_TYPE, {"type": self.type, "sid":self.sid})
        else:
            self.SendMessage(ACTION_SET_TYPE, {"type": self.type})
        self.messageHandler({"socketEvent":CONNECTED_TO_SERVER_EVENT})


    def OnDisconnectWithServer(self):
        print("Disconnected with server")
        self.isConnected = False
        self.messageHandler({"socketEvent":DISCONNECT_WITH_SERVER_EVENT})


    def SendMessage(self, action, data={}):
        if not self.isConnected:
            return
        try:
            data['socketAction'] = action
            msg = json.dumps(data) + EOL

            self.proxyClient.sendall(msg.encode('utf-8'))
        except ConnectionAbortedError as e:
            self.OnDisconnectWithServer()
        except ConnectionResetError as e:
            self.OnDisconnectWithServer()
        except OSError as e:
            self.OnDisconnectWithServer()


    def run(self):
        while True:
            try:
                if self.isConnected:
                    clientMsg = self._ReceiveInput()
                    if(clientMsg==None):
                        continue
                    for msg in clientMsg:
                        if (msg == None):
                            continue

                        self.messageHandler(msg)
            except:
                traceback.print_exc()
        self.proxyClient.close()

    def _ReceiveInput(self):
        if not self.isConnected:
            return

        try:
            clientInput = self.proxyClient.recv(self.maxBufferSize)
        except ConnectionAbortedError as e:
            self.OnDisconnectWithServer()
            return
        except ConnectionResetError as e:
            self.OnDisconnectWithServer()
            return
        except OSError as e:
            self.OnDisconnectWithServer()
            return

        clientInputSize = sys.getsizeof(clientInput)

        if clientInputSize > self.maxBufferSize:
            self.isLongMessage = True
            #print("The input size is greater than expected {}".format(clientInputSize))

        decodedInput = clientInput.decode("utf8").rstrip()  # decode and strip end of line
        result = self._ProcessInput(decodedInput)

        return result

    def _ProcessInput(self, inputStr):
        self.lastMessage += inputStr

        output = []
        input = self.lastMessage.split(EOL)

        if(self.lastMessage[-len(EOL):] != EOL):
            self.lastMessage = input[-1]
            del input[-1]
        else:
            self.lastMessage = ""
            if self.isLongMessage:
                self.isLongMessage = False
                print("Long message end")

        for s in input:
            if(s is not""):
                output.append(json.loads(str(s)))
        return output


    def Close(self):
        self.isAlive = False


class SocketConnectionThread(threading.Thread):
    def __init__(self, connection, address, serverSocket, proxyFunctions):
        print("SocketConnectionThread")
        super(SocketConnectionThread, self).__init__()
        self.maxBufferSize = 2000
        self.connection = connection
        self.address = address
        self.serverSocket = serverSocket
        self.proxyFunctions = proxyFunctions
        self.isAlive = True
        self.lastMessage = ""
        self.type = TYPE_ALL
        self.sid = -1

    def SendMessage(self, action, data={}):
        if not self.isAlive:
            return

        try:
            data['socketEvent'] = action
            msg = json.dumps(data) + EOL

            self.connection.sendall(msg.encode('utf-8'))
        except ConnectionAbortedError as e:
            self.proxyFunctions["On_ClientDisconnect"](self)
            self.Close()
        except ConnectionResetError as e:
            traceback.print_exc()
            self.Close()
        except:
            traceback.print_exc()
            self.Close()
            return

    def run(self):
        while self.isAlive:
            clientMsg = self._ReceiveInput()
            print("Get message from client:", clientMsg)
            if(clientMsg==None):
                break
            for msg in clientMsg:
                if (msg == None):
                    break

                #clientMsg[0] is event name
                if(msg['socketAction']==ACTION_SET_TYPE):
                    self.type = msg['type']
                    if self.type == TYPE_STRATEGY:
                        self.sid = msg['sid']
                else:
                    self.proxyFunctions[msg['socketAction']](msg)

            #self.connection.send(clientMsg.encode('utf-8'))

        self.connection.close()

    def _ReceiveInput(self):
        if not self.isAlive:
            return

        try:
            clientInput = self.connection.recv(self.maxBufferSize)
        except ConnectionAbortedError as e:
            self.proxyFunctions["On_ClientDisconnect"](self)
            return
        except OSError as e:
            self.proxyFunctions["On_ClientDisconnect"](self)
            return

        clientInputSize = sys.getsizeof(clientInput)

        if clientInputSize > self.maxBufferSize:
            print("The input size is greater than expected {}".format(clientInputSize))

        decodedInput = clientInput.decode("utf8").rstrip()  # decode and strip end of line
        result = self._ProcessInput(decodedInput)

        return result

    def _ProcessInput(self, inputStr):
        self.lastMessage += inputStr

        output = []
        input = self.lastMessage.split(EOL)

        if(self.lastMessage[-len(EOL):] != EOL):
            self.lastMessage = input[-1]
            del input[-1]
        else:
            self.lastMessage = ""

        for s in input:
            if(s is not""):
                output.append(json.loads(str(s)))
        return output


    def Close(self):
        print("isAlive set to False")
        #self.connection.close()
        self.isAlive = False


class SocketClientThread(threading.Thread):
    """ Implements the threading.Thread interface (start, join, etc.) and
        can be controlled via the cmd_q Queue attribute. Replies are
        placed in the reply_q Queue attribute.
    """
    def __init__(self, cmd_q=None, reply_q=None):
        super(SocketClientThread, self).__init__()
        self.cmd_q = cmd_q or Queue.Queue()
        self.reply_q = reply_q or Queue.Queue()
        self.alive = threading.Event()
        self.alive.set()
        self.socket = None

        self.handlers = {
            ClientCommand.CONNECT: self._handle_CONNECT,
            ClientCommand.CLOSE: self._handle_CLOSE,
            ClientCommand.SEND: self._handle_SEND,
            ClientCommand.RECEIVE: self._handle_RECEIVE,
        }

    def run(self):
        while self.alive.isSet():
            try:
                # Queue.get with timeout to allow checking self.alive
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type](cmd)
            except Queue.Empty as e:
                continue

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def _handle_CONNECT(self, cmd):
        try:
            self.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((cmd.data[0], cmd.data[1]))
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_CLOSE(self, cmd):
        self.socket.close()
        reply = ClientReply(ClientReply.SUCCESS)
        self.reply_q.put(reply)

    def _handle_SEND(self, cmd):
        header = struct.pack('<L', len(cmd.data))
        try:
            self.socket.sendall(header + cmd.data)
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_RECEIVE(self, cmd):
        try:
            header_data = self._recv_n_bytes(4)
            if len(header_data) == 4:
                msg_len = struct.unpack('<L', header_data)[0]
                data = self._recv_n_bytes(msg_len)
                if len(data) == msg_len:
                    self.reply_q.put(self._success_reply(data))
                    return
            self.reply_q.put(self._error_reply('Socket closed prematurely'))
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _recv_n_bytes(self, n):
        """ Convenience method for receiving exactly n bytes from
            self.socket (assuming it's open and connected).
        """
        data = ''
        while len(data) < n:
            chunk = self.socket.recv(n - len(data))
            if chunk == '':
                break
            data += chunk
        return data

    def _error_reply(self, errstr):
        return ClientReply(ClientReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return ClientReply(ClientReply.SUCCESS, data)