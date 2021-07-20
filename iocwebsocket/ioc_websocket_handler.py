import json
import logging
import tornado.websocket
from utilities.ioc_stardog import IoCStardog

class IoCWebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected")

    def on_close(self):
        logging.info("A client disconnected")
        self.database.close()

    # TODO
    def on_message(self, message):
        logging.info("message: {}".format(message))
        msg_dict = json.loads(message)
        if msg_dict["type"] == "Query":
            self.query_the_database(msg_dict["query"])
            print("QUERYING!")
        elif msg_dict["type"] == "Connect":
            self.connect_to_database(msg_dict["conn_details"])
            print("CONNECTING!")
        else:
            pass

    def connect_to_database(self, conn_details):
        self.database = IoCStardog(conn_details)
        self.database.connect()
        self.write_message("Connection established.")

    def query_the_database(self, query_string):
        response = self.database.query(query_string)
        # logging.info(response)
        self.write_message(response)
