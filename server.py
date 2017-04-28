#Copyright [2017] [Maria Pardo]
#Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
#except in compliance with the License. You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software distributed under the License
#is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied. See the License for the specific language governing
#permissions and limitations under the License.

import socketserver
import http.server
import web

socketserver.TCPServer.allow_reuse_address=True
#WEB SERVER
PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler
Handler =web.testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

"client=web.OpenFDAClient()" #una vez que tenemos el cliente,se conecta al puerto 8000, llega al servidor, y va al Handler. Entonces este codigo se lleva a fichero web.py"
