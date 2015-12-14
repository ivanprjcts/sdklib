import os


class Cookie(object):

    COOKIE_HEADER = "set-cookie"

    def __init__(self, headers):

        if "set-cookie" in headers:
            self.cookie_header = headers["set-cookie"]

    @staticmethod
    def _read_var(file_path):
        content = ""
        if os.path.isfile(file_path):
            f = open(file_path, "r")
            content = f.read()
            f.close()
        return content

    @staticmethod
    def get(var, cookie_content):
        begin = cookie_content.find(var)
        i = cookie_content.find("=", begin)
        e = cookie_content.find(";", i)
        return cookie_content[i+1:e]

    @staticmethod
    def _save_var(value, file_path):
        f = open(file_path, "w")
        f.write(value)
        f.close()

    def set_cookie(self, value):
        self.add_cookie = value
