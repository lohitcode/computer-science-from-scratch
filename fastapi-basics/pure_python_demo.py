#!/usr/bin/env python3
"""
🔴 BEFORE: Pure Python HTTP Server (The Hard Way)
=================================================

This is what writing an API looks like WITHOUT FastAPI.

Run: python3 pure_python_demo.py
Visit: http://localhost:8000/
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HardWayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the path manually
        if self.path == "/":
            response = {"message": "Hello World"}
        elif self.path == "/users":
            response = {"users": ["Alice", "Bob"]}
        elif self.path.startswith("/users/"):
            # Extract user_id from path manually
            user_id = self.path.split("/")[-1]
            response = {"user_id": user_id, "name": "Alice"}
        else:
            response = {"error": "Not found"}

        # Send headers
        self.send_response(200 if self.path != "/notfound" else 404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Convert dict to JSON bytes manually
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        # Read body length manually
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse JSON manually
        try:
            data = json.loads(post_data.decode())
            response = {"created": data}
        except:
            response = {"error": "Invalid JSON"}

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == "__main__":
    print("🔴 Running the HARD WAY (pure Python)...")
    print("Visit: http://localhost:8000/")
    print("Press Ctrl+C to stop\n")

    server = HTTPServer(('localhost', 8000), HardWayHandler)
    server.serve_forever()
