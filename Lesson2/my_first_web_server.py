import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

class WebServerHandler(BaseHTTPRequestHandler):
    form_html = b"""
        <form method='POST' enctype='multipart/form-data' action='/hello'
        <h2>What would you like me to say?</h2>
        <input name='message' type='text'>
        <input type='submit' value='submit'></form>
        """
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()

                output = b""
                output += b"<html><body>Hello!"
                output += b"<a href='/hola'> Go to Hola</a>"
                output += self.form_html
                output += b"</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()

                output = b""
                output += b"<html><body>&#161Hola!"
                output += b"<a href='/hello'> Go to Hello</a>"
                output += self.form_html
                output += b"</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        #try:
        self.send_response(301)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers["content-type"])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == "multipart/form-data":
            fields = cgi.parse_multipart(self.rfile, pdict)
            message_content = fields.get("message")

        output = b""
        output += b"<html><body>"
        output += b"<h2> Okay, how about this: </h2>"
        output += b"<h1> %s </h1>" % message_content[0]
        output += self.form_html
        output += b"</body></html>"
        self.wfile.write(output)
        print(output)
        #except:
         #   pass

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