import http.server
import socketserver
import threading
import time
import os

from commands import commands
from search import search

######################
# Configuration area #
######################

squid_hostname = "idrin" # Hostname or IP address of the server which is running squid proxy
squid_port = 3128 # Port of squid (change only if you changed it in squid configuration)
google_domain = ".google.com" # Domain of Google which is opened from your language. Consult readme for more information
yahoo_domain = ".yahoo.com" # Domain of Yahoo which is opened from your language. Consult readme for more information
keyword = "Siri" # This is only used for Google. Who wants to search with Yahoo anyways?

######################

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Set working directory to path of server.py

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        global squid_hostname
        global squid_port
        global google_domain
        global yahoo_domain
        global keyword
        
        parts = self.path.split("?") #Extract requested file and get parameters from path
        path = parts[0]
        
        #Extract variables from get parameters
        try:
            arguments = {}
            arguments["q"] = None #Variable for search request. Default None to prevent errors if no search request was started
            if (len(parts) > 1):
                raw_arguments = parts[1].split("&")
                for raw_argument in raw_arguments[:]:
                    argument = raw_argument.split("=", 1)
                    arguments[argument[0]] = argument[1]
                    if (argument[0] == "p"): # Yahoo uses search?p= so lets copy that to q=, which is what Google uses.
                        arguments["q"] = argument[1]
        except:
            print ("No get parameters")
        
        print (path)
        
        #Decide wether a search or the style.css was requested
        if (path == "/style.css"):
            self.document = open('style.css', 'r').read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(self.document, "utf-8"))
        elif (path == "/proxy.pac"):
            self.document = open('proxy.pac', 'r').read()
            self.document = self.document.replace('<keyword>', keyword.lower(), 1)
            self.document = self.document.replace('<google_domain>', google_domain, 1)
            self.document = self.document.replace('<yahoo_domain>', yahoo_domain, 1)
            self.document = self.document.replace('<squid_host>', squid_hostname, 2)
            self.document = self.document.replace('<squid_port>', str(squid_port), 2)
            self.send_response(200)
            self.send_header('Content-type', 'x-ns-proxy-autoconfig')
            self.end_headers()
            self.wfile.write(bytes(self.document, "utf-8"))
        elif (arguments["q"] != None):
            arguments["q"] = arguments["q"].replace(keyword + '+', '', 1)
            arguments["q"] = arguments["q"].replace('+', ' ')
            arguments["q"] = arguments["q"].replace('! ', '')
            command = commands(self)
            search(command).search(arguments["q"])
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Not found. Please visit <a href="https://github.com/HcDevel/Siri-API/wiki/_pages">https://github.com/HcDevel/Siri-API/wiki/_pages</a>', "utf-8"))

        return

port = 3030
print ("Starting Server...")

exception = True
while (exception == True): #Solves trouble in autostart mode (when network isn't ready)
    try:
        #(Try) to start webserver
        httpd = socketserver.TCPServer(('', port), Handler)
        threading.Thread(target=httpd.serve_forever).start()
        print('Server listening on port ' + str(port) + '...')
        exception = False
    except:
        print ("Error: Webserver can't be started")
        time.sleep (1)

input ("Press enter to exit")
print ("Shutting down server ...")
httpd.shutdown()
httpd.server_close()
