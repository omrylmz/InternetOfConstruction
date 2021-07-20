import logging
import tornado.websocket

class ForgeViewerBWebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        pass

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        # logging.info("message: {}".format(message))
        self.write_message("OMER")