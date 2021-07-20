import logging
import json

from tornado.web import RequestHandler
from tornado.web import StaticFileHandler

class SharePointFileRequestHandler(StaticFileHandler):
    # def __init__(self):
    #     super().__init()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        if not self.current_user:
            self.redirect("/login/")
            return

    # def get(self, option):
    #     if not self.current_user:
    #         self.redirect("/login/")
    #         return
    #     super().get(option)
    #     self.on_finish(option)

    def on_finish(self):
        super().on_finish()
        with open("888888.txt","w+") as f:
            f.write(self.path_args)
        # print("A file named " + option + "is added to the repository!")
