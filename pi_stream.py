import io
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from picamera2 import Picamera2

print("Starting up Live Camera Streaming Module...")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()
time.sleep(2)

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            
            try:
                while True:
                    frame_buffer = io.BytesIO()
                    picam2.capture_file(frame_buffer, format="jpeg")
                    frame_bytes = frame_buffer.getvalue()
                    
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame_bytes))
                    self.end_headers()
                    self.wfile.write(frame_bytes)
                    self.wfile.write(b'\r\n')
                    time.sleep(0.04)
            except Exception as e:
                pass
        else:
            self.send_error(404)
            self.end_headers()

try:
    server_address = ('0.0.0.0', 8000)
    server = HTTPServer(server_address, StreamingHandler)
    print("Live Server Active on Port 8000!")
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    picam2.stop()

