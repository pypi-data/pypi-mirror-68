import inspect
import threading
import websocket
import ssl
import sys
from time import sleep

class MyWebSocket():
	def connect(self, wsURL="wss://www.bitmex.com/realtime?subscribe=quote:XBTUSD"):
		print("Starting thread")
		ssl_defaults = ssl.get_default_verify_paths()
		sslopt_ca_certs = {"ca_certs": ssl_defaults.cafile}
		self.ws = websocket.WebSocketApp(wsURL,
                                         on_message=self.__on_message,
                                         on_close=self.__on_close,
                                         on_open=self.__on_open,
                                         on_error=self.__on_error,
                                         )
		self.wst = threading.Thread(target=lambda: self.ws.run_forever(sslopt=sslopt_ca_certs))
		self.wst.daemon = True
		self.wst.start()

		conn_timeout = 5
		while (not self.ws.sock or not self.ws.sock.connected) and conn_timeout:
			sleep(1)
			conn_timeout -= 1
		if not conn_timeout:
			print("Could not connect to WS! Exiting.")
			sys.exit(1)

	def _callback(self, callback, *args):
         if callback:
            try:
                 if inspect.ismethod(callback):
                     callback(*args)
                 else:
                     callback(self, *args)
            except :
                pass

	def __on_message(self, message):
		print(message)
	def __on_open(self):
		print("opened")
	def __on_close(self):
		print("closed")
	def __on_error(self, error):
		print("error")

websocket.enableTrace(True)
mysocket = MyWebSocket()
mysocket.connect()

while True:
	sleep(1)