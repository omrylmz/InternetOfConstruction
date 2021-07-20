from pathlib import Path
from datetime import datetime
from tornado.web import RequestHandler
from utilities.ioc_converter import IoCConverter

class SharePointFileUploadHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        if not self.current_user:
            self.redirect("/login/")
            return
        print("|||||||||||||||||||||||||||")
        download_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / "Uploads").resolve()
        print(str(download_path))
        self.write(str(download_path) + "\n")
        if self.path_args:
            now_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            file_path = Path(download_path / (self.path_args[0] + "_" + now_str)).resolve() 
            with open(file_path,"w+") as f:
                f.write(str(self.current_user) + "_")


    def get(self, path_arg):
        self.write('<!DOCTYPE html>\
                            <html lang="en">\
                            <head>\
                                <meta charset="UTF-8">\
                                <title>Title</title>\
                            </head>\
                            <body>\
                            <form action="fileup" method="post" enctype="multipart/form-data">\
                                    <input type="file" name="to_be_uploaded_file">\
                                    <input type="file" name="to_be_uploaded_file_2">\
                                    <input type="file" name="to_be_uploaded_img">\
                                                                <input type="submit" value="Upload">\
                                </form>\
                            </body>\
                            </html>')

    def post(self, path_arg):
        print("===========================")
        self.write("Hello! This is the SharePoint upload POST " + path_arg)
        uploaded_file = self.request.files["to_be_uploaded_file"][0]
        print(uploaded_file["filename"])
        print(uploaded_file["body"])

        # file_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / uploaded_file["filename"]).resolve()
        # with open(file_path,"w+") as f:
        #     f.write(uploaded_file["body"])

        # file1 = self.request.files['dummy'][0]
        # original_fname = file1['filename']
        # print(original_fname)
        # # assert(path_arg == original_fname)

        # output_file = open("iocsharepoint/SHAREPOINT/Uploads/" + original_fname, 'wb')
        # output_file.write(file1['body'])

        # self.finish("file " + original_fname + " is uploaded")

    def on_finish(self) -> None:
        super().on_finish()
        print("ON FINISH!!!!!!!!!!!!!!!!!!!")
        # print(self.request.files["to_be_uploaded_file"][0]["body"])
        # Remember this is called also for GET
        if ("to_be_uploaded_file" in self.request.files.keys()):
            uploaded_file = self.request.files["to_be_uploaded_file"][0]
            file_path = Path(Path.cwd() / "iocsharepoint" / "SHAREPOINT" / uploaded_file["filename"]).resolve()

            # converted_file = uploaded_file["body"].decode("ascii") # TODO: Do something here
            converted_file = IoCConverter(uploaded_file["body"].decode("ascii")).convert()

            with open(file_path,"w+") as f:
                f.write(converted_file)