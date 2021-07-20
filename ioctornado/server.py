#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json
import pathlib

import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.httpserver import HTTPServer
from tornado.web import url, StaticFileHandler, RedirectHandler

from utilities.ioc_login_handler import IoCLoginHandler

from iocsharepoint.share_point_request_handler import SharePointRequestHandler
from iocsharepoint.share_point_a_request_handler import SharePointARequestHandler
from iocsharepoint.share_point_file_request_handler import SharePointFileRequestHandler
from iocsharepoint.share_point_file_upload_handler import SharePointFileUploadHandler
from iocsharepoint.share_point_file_download_handler import SharePointFileDownloadHandler

from iocwebsocket.ioc_websocket_handler import IoCWebSocketHandler
from iocwebsocket.iocforgeviewer.forge_viewer_websocket_handler import ForgeViewerWebSocketHandler
from iocwebsocket.iocforgeviewer.forge_viewer_a_websocket_handler import ForgeViewerAWebSocketHandler
from iocwebsocket.iocforgeviewer.forge_viewer_b_websocket_handler import ForgeViewerBWebSocketHandler
from iocwebsocket.iocforgeviewer.forge_viewer_c_websocket_handler import ForgeViewerCWebSocketHandler
 

define("port", default=3000, help="Run on the specified port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        static_files_path = pathlib.Path(__file__, "../staticfiles").resolve()

        handlers = [
            (r"/login/", IoCLoginHandler),
            (r"/login", RedirectHandler, {url: "/login/"}),
            (r"/iocsp/file/(.*)/", SharePointFileRequestHandler, {"path": static_files_path}),
            (r"/iocsp/file/(.*)", RedirectHandler, {url: "/iocsp/file/(.*)/"}),
            (r"/iocsp/upload/(.*)/fileup", SharePointFileUploadHandler),
            (r"/iocsp/upload/(.*)/", SharePointFileUploadHandler),
            (r"/iocsp/upload/(.*)", RedirectHandler, {url: "/iocsp/upload/(.*)/"}),
            (r"/iocsp/download/(.*)/", SharePointFileDownloadHandler),
            # (r"/iocsp/download/(.*)", SharePointFileDownloadHandler),
            # (r"/iocsp/download/(.*)", RedirectHandler, {url: "/iocsp/download/{1}/"}),
            (r"/iocsp/(.*)/", SharePointRequestHandler),
            (r"/iocsp/(.*)", RedirectHandler, {url: "/iocsp/(.*)/"}),
            (r"/iocsp/a/(.*)/", SharePointARequestHandler),
            (r"/iocsp/a/(.*)", RedirectHandler, {url: "/iocsp/a/(.*)/"}),
            (r"/iocws/forgeviewer/a/", ForgeViewerAWebSocketHandler),
            (r"/iocws/forgeviewer/a", RedirectHandler, {url: "/iocws/forgeviewer/a/"}),
            (r"/iocws/forgeviewer/b/", ForgeViewerBWebSocketHandler),
            (r"/iocws/forgeviewer/b", RedirectHandler, {url: "/iocws/forgeviewer/b/"}),
            (r"/iocws/forgeviewer/c/", ForgeViewerCWebSocketHandler),
            (r"/iocws/forgeviewer/c", RedirectHandler, {url: "/iocws/forgeviewer/c/"}),
            (r"/iocws/forgeviewer/", ForgeViewerWebSocketHandler),
            (r"/iocws/forgeviewer", RedirectHandler, {url: "/iocws/forgeviewer/"}),
            (r"/iocws/", IoCWebSocketHandler),
            (r"/iocws", RedirectHandler, {url: "/iocws/"}),
        ]

        settings = {
            "debug": True,
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
        }

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
