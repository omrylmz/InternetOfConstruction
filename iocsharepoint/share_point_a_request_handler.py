from tornado.web import RequestHandler

class SharePointARequestHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        if not self.current_user:
            self.redirect("/login/")
            return

    def get(self, option):
        self.write("Hello GET! " + option)

    def post(self, option):
        self.write("Hello POST!" + option)