import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, Restaurant, MenuItem

class WebServerHandler(BaseHTTPRequestHandler):
    edit_html = b"""
        <form method='POST' enctype='multipart/form-data'
        <h2>Please enter the new restaurant name: </h2>
        <input name='message' type='text'>
        <input type='submit' value='Submit'></form>
        """
    delete_html = b"""
        <form method='POST' enctype='multipart/form-data'
        <h2>Are you sure you want to delete the restaurant? </h2>
        <input type='submit' name='button' value='Yes'>
        <input type='submit' name='button' value='No'></form>
        """
    engine = create_engine('sqlite:///db/restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                restaurants = self.session.query(Restaurant).all()
                output = b""
                output += b"<html><body>"
                for restaurant in restaurants:
                    name = bytes(restaurant.name, "utf-8")
                    id = bytes(str(restaurant.id), "utf-8")
                    output += b"<a href='/%s/menu'><b>%s</b></a><br>" % (id, name)
                    output += b"<a href='/%s/edit'>Edit</a><br>" % id
                    output += b"<a href='/%s/delete'>Delete</a><br>" % id
                    output += b"<br><br>"
                output += b"<a href='/new'><b>Add a new restaurant</b></a>"
                output += b"</body></html>"
                self.wfile.write(output)
                print(output)
                return
            elif self.path.endswith("/menu"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                id = int(self.path.split("/")[1])
                return
            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                id = int(self.path.split("/")[1])
                restaurant = self.session.query(Restaurant).filter_by(id=id).one()
                name = bytes(restaurant.name, "utf-8")
                output = b"<html><body>"
                output += b"<b>%s</b><br>" % name
                output += self.edit_html
                output += b"</body></html>"
                self.wfile.write(output)
                print(output)
                return
            elif self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                id = int(self.path.split("/")[1])
                restaurant = self.session.query(Restaurant).filter_by(id=id).one()
                name = bytes(restaurant.name, "utf-8")
                output = b"<html><body>"
                output += b"<b>%s</b><br>" % name
                output += self.delete_html
                output += b"</body></html>"
                self.wfile.write(output)
                print(output)
                return
            elif self.path.endswith("/new"):
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                output = b"<html><body>"
                output += self.edit_html
                output += b"</body></html>"
                self.wfile.write(output)
                print(output) 
                return               
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        if self.path.endswith("/edit"):
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers["content-type"])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                message_content = fields.get("message")
            id = int(self.path.split("/")[1])
            restaurant = self.session.query(Restaurant).filter_by(id=id).one()
            restaurant.name = message_content[0].decode("utf-8")
            self.session.add(restaurant)
            self.session.commit()
            return
        elif self.path.endswith("/delete"):
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers["content-type"])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                answer = fields["button"][0].decode("utf-8")
                if answer == "Yes":
                    id = int(self.path.split("/")[1])
                    restaurant = self.session.query(Restaurant).filter_by(id=id).one()
                    self.session.delete(restaurant)
                    self.session.commit()
            return
        elif self.path.endswith("/new"):
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers["content-type"])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                message_content = fields.get("message")
            restaurant = Restaurant(name=message_content[0].decode("utf-8"))
            self.session.add(restaurant)
            self.session.commit()
            return

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