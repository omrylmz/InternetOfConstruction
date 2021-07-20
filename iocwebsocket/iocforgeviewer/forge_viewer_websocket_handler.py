import logging
import stardog
import tornado.websocket
from iocwebsocket.ioc_websocket_handler import IoCWebSocketHandler

class ForgeViewerWebSocketHandler(IoCWebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected")

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))