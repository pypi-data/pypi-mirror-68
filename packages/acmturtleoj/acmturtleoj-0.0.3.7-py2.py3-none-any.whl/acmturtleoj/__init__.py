import os
import sys
import subprocess
from threading import Thread
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
from urllib.parse import urlparse
import json
import ssl
from acmturtleoj import oj

data = { "result": "ok" }
pong = { "result": "pong" }
err = { "result": "error" }
server_address = ('localhost', 4443)

# 加载模板到内存
template = oj.load_template()

class CORSRequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        referer = self.headers['Referer']
        refUri = urlparse(referer)
        self.send_response(200)
        #if refUri.netloc.endswith('.acmcoder.com'):
        #    self.send_header('Access-Control-Allow-Origin', refUri.scheme + '://' + refUri.netloc)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        path = self.path
        if path == '/ping':
            self.wfile.write(json.dumps(pong).encode())
        elif path.startswith('/run?'):
            self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])
            params = urllib.parse.parse_qs(self.queryString)
            if 'user_id' in params and 'guid' in params and 'solution_id' in params:
                oj.main(params['user_id'][0], params['guid'][0], params['solution_id'][0], template)
                self.wfile.write(json.dumps(data).encode())
            else:
                self.wfile.write(json.dumps(err).encode())
        else:
            self.wfile.write(json.dumps(data).encode())

def main():
    """
    python3 = sys.executable
    result = subprocess.Popen('"' + python3 + '" -V', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    win = result.stdout.read().decode('utf-8')
    print(win)
    """
    try:
        key = oj.load_key()
        pem = oj.load_pem()
        svg_turtle_py = oj.load_svg_turtle()
        oj.write_file('web.key', key)
        oj.write_file('web.pem', pem)
        oj.write_file('svg_turtle.py', svg_turtle_py)
        httpd = HTTPServer(server_address, CORSRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                    server_side=True,
                                    certfile='web.pem',
                                    keyfile='web.key',
                                    ssl_version=ssl.PROTOCOL_TLSv1)
        print("The OJ Client starts succ， Please go to write your code!")
        httpd.serve_forever()
    except KeyboardInterrupt as ke:
        print('exit by your input')
    except Exception as e:
        print('exit')
    finally:
        os.remove('web.pem')
        os.remove('web.key')
        os.remove('svg_turtle.py')