import websocket

class MySocket(object):
    def __init__(self):
        pass

    def connect(self):
        print("Startating thread")
        websocket.enableTrace(True)
        self.websocketapp = websocket.WebSocketApp("wss://ws.finnhub.io?token=bqi6c5frh5rbubolumn0",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)

    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print( "### closed ###")


    def on_open(self):
        self.websocketapp.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    mys = MySocket()
    mys.websocketapp.run_forever()
