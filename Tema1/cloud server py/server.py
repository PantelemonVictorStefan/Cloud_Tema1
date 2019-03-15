import http.server
import socketserver
import urllib.request
import json
import os
import time

PORT = 8000


logs=[]
def loadLogs():
    global logs
    if(os.path.exists("logs.json")):
        fd=open("logs.json","r")
        logs=json.load(fd)
        fd.close()
    else:
        logs=[]
def saveLogs():
    global logs
    fd=open("logs.json","w")
    json.dump(logs,fd)
    fd.close()

def log(request,response,latency):
    global logs
    loadLogs()
    logs.append((request,response,latency))

    saveLogs()


def createResponse(filename,response):
    fd=open(filename,"w+")
    fd.write(response)
    fd.close()

def createBin(filename,response):
    fd = open(filename, "wb+")
    fd.write(response)
    fd.close()



def getRandomPersonApi():
    latency = time.time()
    url="https://randomuser.me/api/"
    response=urllib.request.urlopen(url)
    content=response.read()
    latency =  time.time()-latency
    log(url, content.decode("utf-8"), latency)
    createResponse("response.json",(content.decode("utf-8")))

def generateImageApi():
    latency=time.time()
    url="https://thispersondoesnotexist.com/image"
    response = urllib.request.urlopen(url)
    content = response.read()
    latency=time.time()-latency
    log(url,"https://thispersondoesnotexist.com/image",latency)
    createBin("response.jpg", content)



class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/getRandomPerson':
            getRandomPersonApi()
            self.path = "/response.json"

        if self.path == '/generateImage':
            generateImageApi()
            self.path="/response.jpg"


        return http.server.SimpleHTTPRequestHandler.do_GET(self)

#Handler = http.server.SimpleHTTPRequestHandler

def runServer():
    Handler = MyRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        httpd.serve_forever()

runServer()
#getRandomPersonApi()
#generateImageApi()
