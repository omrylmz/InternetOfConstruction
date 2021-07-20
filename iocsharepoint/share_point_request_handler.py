from tornado.web import RequestHandler
from pathlib import Path
from datetime import datetime

class SharePointRequestHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        if not self.current_user:
            self.redirect("/login/")
            return
        # print("|||||||||||||||||||||||||||")
        # download_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / "Downloads").resolve()
        # print(str(download_path))
        # self.write(str(download_path) + "\n")
        # if self.path_args:
        #     now_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        #     file_path = Path(download_path / (self.path_args[0] + "_" + now_str)).resolve() 
        #     with open(file_path,"w+") as f:
        #         f.write(str(self.current_user) + "_")


    def get(self, path_arg):
        self.write("Hello! This will be the main SharePoint page! " + path_arg)

    def post(self, path_arg):
        self.write("Hello POST! " + path_arg)