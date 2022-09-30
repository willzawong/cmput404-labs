#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # https://stackoverflow.com/a/606199, Aaron Maenpaa
        split = (self.data.decode("utf-8").split(" "))
        method = split[0]

        not_allowed_methods = ["POST","PUT","DELETE"]
        if(method in not_allowed_methods):
            self.request.sendall("HTTP/1.1 405 Method Not Allowed".encode())
        elif(method == "GET"):
            http_response_str = "HTTP/1.1 200 OK\r\n"

            # https://stackoverflow.com/a/7166139, Russ, 2022-09-28
            file_dir = os.path.dirname(__file__)
            file_dir = os.path.join(file_dir,"www")
            file_dir = file_dir.replace("\\","/")
            filepath = split[1]
            filepath = filepath.replace("\\","/")

            # make sure you cannot send files outside of the www folder
            if("/../" in filepath):
                self.request.sendall("HTTP/1.1 404 Not Found".encode())

            # handle redirection
            if not "." in filepath:
                if(filepath[-1:] != "/"):
                    filepath += "/"
                    http_response_str = "HTTP/1.1 301 Moved Permanently\r\n"
                    http_response_str += "Location: http://127.0.0.1:8080" + filepath +"\r\n"
            if(filepath[-1:] == "/"):
                filepath += "index.html"
            try:
                # https://stackoverflow.com/a/38861808, James, 2022-09-26
                # https://stackoverflow.com/questions/24728088/python-parse-http-response-string, fix
                with open(file_dir+filepath) as f:
                    # send css only if it asks for css only
                    if(filepath[-3:] == "css"):
                        http_response_str += """Content-Type: text/css\r\n"""
                        http_response_str = http_response_str + f.read()
                        self.request.sendall(http_response_str.encode())
                    else:
                        # check what css to send
                        cssfile = "base.css"
                        if("/deep" in filepath):
                            cssfile="deep/deep.css"

                        # send html and css
                        with open(file_dir+filepath) as f, open(file_dir+'/'+cssfile) as css:
                            http_response_str += """Content-Type: text/html\r\n"""
                            self.request.sendall(http_response_str.encode())
                            self.request.sendall(("".join(f.readlines())).encode())
                            http_response = """\n<style type="text/css">\n""" +css.read() + "\n"
                            self.request.sendall(http_response.encode())
            except Exception as e:
                # throw error if file is not found...
                print(e)
                self.request.sendall("HTTP/1.1 404 Not Found".encode())
            pass
        else:
            self.request.sendall("HTTP/1.1 404 Not Found".encode())        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
