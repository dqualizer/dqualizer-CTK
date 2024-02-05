# At least on Windows venv seems to be missing in PYTHONPATH after venv activation, so we add it to find
# modules
import os
import sys
current_script_path = os.path.abspath(__file__)
current_project_path = os.path.abspath(
    os.path.join(current_script_path, os.pardir, os.pardir, os.pardir))

running_on_linux = os.name != "nt"
venv_path = os.path.join(current_project_path, 'venv', 'lib', 'python3.10', 'site-packages') if running_on_linux else os.path.join(current_project_path, 'venv', 'Lib', 'site-packages')
sys.path.insert(0, venv_path)
print(sys.path)


from http.server import SimpleHTTPRequestHandler
import time
from processMonitoring import check_process_exists

processNameToCheck = "KeePassXC.exe"


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print("\nHeaders received:")
        for key, value in self.headers.items():
            print(f"{key}: {value}")

        if check_process_exists(processNameToCheck, False):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Connection', 'close')  # Disable keep-alive Connections
            self.end_headers()

            # Send the response content
            response_content = 'This is a quickly answered request, because the process ' + processNameToCheck + (
                ' is present.')
            print(f"Answering request with QUICK response")
            self.wfile.write(response_content.encode('utf-8'))

        else:
            # Introduce a delay of 2 seconds (adjust as needed)
            time.sleep(2)

            # Send the HTTP response headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Connection', 'close')  # Disable keep-alive Connections
            self.end_headers()

            # Send the response content
            response_content = 'This is a slowly answered request, because the process ' + processNameToCheck + (
                'is NOT present.')
            print(f"Answering request with SLOW response")
            self.wfile.write(response_content.encode('utf-8'))


if __name__ == "__main__":
    from http.server import HTTPServer

    port = 3000
    server_address = ('', port)

    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print(f"Serving on port {port}")
    httpd.serve_forever()
