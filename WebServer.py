
import multiprocessing
import re
import socket
import json
import urllib3


class WebServer(object):

    def __init__(self, port):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind(("", port))
        self.__server_socket.listen(128)

    def __client_handle(self, client_socket, module):
        recv_data = client_socket.recv(4096)
        request_data = recv_data.decode('utf-8')
        request_line = request_data.splitlines()
        self.request_file = re.match(r"[^/]+(/[^ ]*)", request_line[0]).group(1)
        print(self.request_file)

        if self.request_file:
            if self.request_file == "/":
                self.request_file = "/index.html"

        if self.request_file.endswith(".html"):
            env = {"PATH_INFO": self.request_file}
            file = module.application(env, self.__get_status)
            header = "HTTP/1.1 %s\r\n" % self.__status
            for i in self.__parmas:
                header += "%s:%s\r\n" % i
            data = header + "\r\n" + file
            client_socket.send(data.encode("utf-8"))
        else:
            try:
                with open("./static" + self.request_file, 'rb') as f:
                    html_file = f.read()
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                client_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                client_socket.send(html_file)
            except:
                # 如果没找到,拼接响应信息并返回信息
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                with open('./templates/error.html', 'r') as f:
                    file = f.read()
                response += file
                client_socket.send(response.encode("utf-8"))
        client_socket.close()

    def __get_status(self, status, parmas):
        self.__status = status
        self.__parmas = parmas

    def run(self, module):
        while True:
            client_socket, addr = self.__server_socket.accept()
            p1 = multiprocessing.Process(target=self.__client_handle, args=(client_socket, module))
            p1.start()

            client_socket.close()


def main():
    with open("./dynamic/UserSet.conf", "r") as f:
        dict_str = f.read()

    dict_str = eval(dict_str)
    port = dict_str["port"]
    mod_str = dict_str["module"]
    import sys
    sys.path.append("dynamic")
    module = __import__(mod_str)
    webServer = WebServer(port)
    webServer.run(module)


if __name__ == "__main__":
    main()
