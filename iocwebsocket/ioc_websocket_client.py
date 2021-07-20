#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import asyncio
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class IoCWebSocketClient(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ws = None
        # PeriodicCallback(self.keep_alive, 20000).start()

    async def create(url, timeout):
        client = IoCWebSocketClient(url, timeout)
        return client

    async def connect(self):
        print("trying to connect")
        try:
            self.ws = await websocket_connect(self.url)
        except Exception as e:
            print("Connection error")
        else:
            print("Connected to the websocket")

    async def connect_to_database(self, conn_details):
        msg_dict = {"type": "Connect", "conn_details": conn_details}
        self.ws.write_message(json.dumps(msg_dict))
        msg = await self.ws.read_message()
        if msg is None:
            print("Couldn't connect to the database")
            self.ws = None
        else:
            print(msg)

    async def query(self, query_string):
        msg_dict = {"type": "Query", "query": query_string}
        self.ws.write_message(json.dumps(msg_dict))
        return await self.ws.read_message()

    async def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

    async def close(self):
        self.ws.close()