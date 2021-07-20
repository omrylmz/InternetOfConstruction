from tornado.web import RequestHandler


class IoCLoginHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.write('<html><body><form action="/login/" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        print("=========================")
        print(self.get_argument("name"))
        self.redirect("/iocsp/" + self.get_argument("name") + "/")
