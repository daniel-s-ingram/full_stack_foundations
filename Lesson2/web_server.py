import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = b""
                output += b"<html><body>Hello!</body></html>"
                output += b"<a href='/hola'> Go to Hola</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = b""
                output += b"<html><body>&#161Hola!"
                output += b"<a href='/hello'> Go to Hello</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, 
                "File Not Found {}".format(self.path))

        def do_POST(self):
            try:
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cg.parse_header(
                    self.headers.getheader("content-type"))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multiparse(self.rfile, pdict)
                    message_content = fields.get("message")

                output = b""
                output += b"<html><body>"
                output += b"<h2> Okay, how about this: </h2>"
                output += b"<h1> {} </h1>".format(message_content[0])
                output += b"<form method='POST' "
                output += b"enctype='multipart/form-data'"
                output += b"action='/hello'>"
                output += b""
            except:
                pass

def main():
    try:
        port = 8080
        server = HTTPServer(('localhost', port), WebServerHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping web server...")
        server.socket.close()

if __name__ == "__main__":
    main()