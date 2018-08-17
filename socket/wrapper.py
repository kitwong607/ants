class EWrapper:
    def logAnswer(self, fnName, fnParams):
        if logging.getLogger().isEnabledFor(logging.INFO):
            if 'self' in fnParams:
                prms = dict(fnParams)
                del prms['self']
            else:
                prms = fnParams
            logging.info("ANSWER %s %s", fnName, prms)


    def error(self, errorCode:int, errorString:str):
        """This event is called when there is an error with the
        communication or when TWS wants to send a message to the client."""

        self.logAnswer(current_fn_name(), vars())
        logging.error("ERROR %s %s", errorCode, errorString)


    def winError(self, text:str, lastError:int):
        self.logAnswer(current_fn_name(), vars())


    def connectionClosed(self):
        """This function is called when TWS closes the sockets
        connection with the ActiveX control, or when TWS is shut down."""

        self.logAnswer(current_fn_name(), vars())