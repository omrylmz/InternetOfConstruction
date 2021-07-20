from tornado.web import HTTPError, RequestHandler
from pathlib import Path
from datetime import datetime

class   SharePointFileDownloadHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        if not self.current_user:
            self.redirect("/login/")
            return
        print("|||||||||||||||||||||||||||")
        download_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / "Downloads").resolve()
        print(str(download_path))
        self.write(str(download_path) + "\n")
        if self.path_args:
            now_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            print(self.path_args[0])
            file_path = Path(download_path / (self.path_args[0] + "_" + now_str)).resolve() 
            with open(file_path,"w+") as f:
                f.write(str(self.current_user) + "_")


    def get(self, file_name):
        # What about file extension?
        self.write("Hello! This is the SharePoint download GET " + file_name)
        file_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / file_name).resolve()
        if not file_name or not Path.exists(file_path):
            raise HTTPError(404)
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % file_name)    
        with open(file_path, "rb") as f:
            try:
                while True:
                    _buffer = f.read(4096)
                    if _buffer:
                        self.write(_buffer)
                    else:
                        f.close()
                        self.finish()
                        return
            except:
                raise HTTPError(404)
        raise HTTPError(500)

    def post(self, path_arg):
        self.write("Hello! This is the SharePoint download POST " + path_arg)