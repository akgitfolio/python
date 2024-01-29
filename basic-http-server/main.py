from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

class DeviceDiscoveryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        devices = [{"id": 1, "name": "Device 1"}, {"id": 2, "name": "Device 2"}]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(devices).encode('utf-8'))

def run_discovery_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, DeviceDiscoveryHandler)
    print('Starting device discovery server on port 8000...')
    httpd.serve_forever()

discovery_thread = Thread(target=run_discovery_server)
discovery_thread.daemon = True
discovery_thread.start()

@socketio.on('device_control')
def handle_device_control(data):
    print(f"Received control data: {data}")
    emit('control_confirmation', {'status': 'success', 'data': data})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
