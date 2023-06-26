from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from http import HTTPStatus


# Define the directory where your images are stored
image_directory = 'images'

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Image-Name')
        self.end_headers()    

    def do_GET(self):
        try:
            # Get the filename from the URL
            filename = self.path[1:]
            filepath = os.path.join(image_directory, filename)

            # Open the file in binary mode and read its contents
            with open(filepath, 'rb') as file:
                content = file.read()

            # Send the response header
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')

            # Enable CORS by setting the Access-Control-Allow-Origin header
            self.send_header('Access-Control-Allow-Origin', '*')

            self.end_headers()

            # Send the file content as the response body
            self.wfile.write(content)

        except IOError:
            # Send a 404 error if the file is not found
            self.send_error(404, 'File Not Found: {}'.format(self.path))

    def do_POST(self):
        if self.path == '/images':
            print("post connected")


            content_length = int(self.headers['Content-Length'])
            image_data = self.rfile.read(content_length)

            # Extract user hash from headers or request parameters
            filename = self.headers.get('Image-Name')  # Assuming User-Hash is in the request headers

            # Get the filename from the 'filename' field in the request headers
            image_directory = 'images'

            # Save the image with a unique filename
            filepath = os.path.join(image_directory, filename)

            # Save the image to the specified filepath
            with open(filepath, 'wb') as file:
                file.write(image_data)

               
            # Send a response
            self.send_response(HTTPStatus.OK)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Image-Name')  # Allow 'Listing-Hash' header
            self.end_headers()
            self.wfile.write(b"Image uploaded successfully.")




def run(server_class=HTTPServer, handler_class=RequestHandler, port=7000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting cdn.py on port {}...'.format(port))
    httpd.serve_forever()

# Run the server
if __name__ == '__main__':
    run()
