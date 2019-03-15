import http.server
import socketserver
import urllib.request
import json
import os
import urllib.parse
from http import cookies
import random
import time


PORT = 8000




def createResponse(filename,response):
    fd=open(filename,"w+")
    fd.write(response)
    fd.close()

def createBin(filename,response):
    fd = open(filename, "wb+")
    fd.write(response)
    fd.close()






def saveCollection(collection,collectionName):
    fd = (open(collectionName, "w+"))
    json.dump(collection,fd)
    fd.close()

def getCollection(collection):
    fd=(open(collection,"r"))
    ob=json.load(fd)
    fd.close()
    return ob



def loadUsers():
    global users
    if os.path.exists("data/users.json"):
        users=getCollection("data/users.json")
    else:
        users=[]

def saveUsers():
    global users
    saveCollection(users,"data/users.json")

def userExists(user):
    global users
    loadUsers()
    if user in users:
        return True
    return False

def usernameExists(user):
    global users
    loadUsers()
    usernames=[]
    for i in users:
        usernames.append(i["username"])
    if user["username"] in usernames:
        return True
    return False


def addUser(user):
    global users
    loadUsers()
    if usernameExists(user):
        return False
    users.append(user)
    saveUsers()
    return True


def removeUser(user):
    global users
    if userExists(user):
        users.remove(user)
        saveUsers()
        return True
    return False

def loadPosts():
    global posts
    if os.path.exists("data/posts.json"):
        posts=getCollection("data/posts.json")
    else:
        posts=dict()

def savePosts():
    global posts
    saveCollection(posts,"data/posts.json")

def addPost(post):
    global posts
    if(post["title"] in posts.keys()):
        return False
    posts[post["title"]]=post
    savePosts()
    return True

def deletePost(post):
    global posts
    if (post["title"] in posts.keys()):
        #print(posts)
        del posts[post["title"]]
        #print(posts)
        savePosts()
        return True
    return False


def checkSession(session):
    global openSessions
    availability=3600
    for key in openSessions.keys():
        if(time.time()-openSessions[key][0]>availability):
            openSessions.pop(key,None)
    if session in openSessions.keys():
        return True
    return False


def authenticateUser(user,sessionId):
    global users
    global openSessions

    if(userExists(user)):
        openSessions[sessionId]=(time.time(),user["username"])
        return True
    return False


def getUser(sessionId):
    global openSessions
    if(sessionId in openSessions.keys()):
        return openSessions[sessionId][1]
    return None




def generateSessionId():
    x=random.getrandbits(128)
    #print(x)
    c = cookies.SimpleCookie()
    c["sessionid"] = x
    return c


def handleRegisterApi(rawData):

    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]

    #print(values.keys())
    if("username" in values.keys() and "password" in values.keys()):
        if(len(values["username"])>0 and len(values["password"])>0):
            if(addUser(values)):
                return 201
            else:
                return 409
    return 400

def handleLoginApi(rawData,sessionId):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    if ("username" in values.keys() and "password" in values.keys()):
        if (len(values["username"]) > 0 and len(values["password"]) > 0):
            if(authenticateUser(values,sessionId)):
                return 200
            else:
                return 401
    return 400

def handleLoginApi2(rawData,sessionId):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    if ("username" in values.keys() and "password" in values.keys()):
        if (len(values["username"]) > 0 and len(values["password"]) > 0):
            if(authenticateUser(values,sessionId)):
                return 200
            else:
                return 401
    return 400




def handleAddPostAPI(rawData,sessionId):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    print(values)
    if ("title" in values.keys() and "text" in values.keys()):
        if (len(values["title"]) > 0 and len(values["text"]) > 0):
            user=getUser(sessionId)
            if(user==None):
                return 403

            post=dict()
            post["title"]=values["title"]
            post["text"] = values["text"]
            post["user"] = user
            post["timestamp"]=time.time()
            print(post)
            if(addPost(post)):
                return 201
            return 409
    return 400

def handleAddPostAPI2(rawData):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    print(values)
    if ("title" in values.keys() and "text" in values.keys()):
        if (len(values["title"]) > 0 and len(values["text"]) > 0):

            post=dict()
            post["title"]=values["title"]
            post["text"] = values["text"]
            post["timestamp"]=time.time()
            print(post)
            if(addPost(post)):
                return 201
            return 409
    return 400

def handleGetPostsAPI(path):
    global posts
    if len(posts)==0:

        return (204, None)
    else:
        query = urllib.parse.urlparse(path).query
        if "=" in query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            for key in query_components:
                query_components[key] = urllib.parse.unquote_plus(query_components[key])
            print(query_components["title"])
            if query_components["title"] in posts.keys():
                content = json.dumps(posts[query_components["title"]])
                return (200, bytearray(content, "utf-8"))
            else:
                return (404, None)
            #if()
            #content=json.json.dumps(posts[query_components["title"]])


        content = json.dumps(posts)
        return (200, bytearray(content, "utf-8"))

def handlePutAPI(rawData):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    print(values)
    if ("title" in values.keys() and "text" in values.keys()):
        if (len(values["title"]) > 0 and len(values["text"]) > 0):
            #user = getUser(sessionId)
            #if (user == None):
            #    return 403

            post = dict()
            post["title"] = values["title"]
            post["text"] = values["text"]
            post["timestamp"] = time.time()
            print(post)
            #nice to have: do not delete if edited post conflicts with another post
            if(deletePost(post)):
                if (addPost(post)):
                    return 204
                return 409
            else:
                return 404
    return 400

def handleChangePasswordAPI(rawData):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    if ("username" in values.keys() and "password" in values.keys() and "newPassword" in values.keys()):
        if (len(values["username"]) > 0 and len(values["password"]) > 0 and len(values["newPassword"]) > 0):
            user=dict()
            user["username"]=values["username"]
            user["password"]=values["password"]
            if removeUser(user):
                user["password"] = values["newPassword"]
                if(addUser(user)):
                    return 200
                else:
                    user["password"] = values["password"]
                    addUser(user)
                    return 500
            else:
                return 401
    return 400

def handleDeleteAPI(path):
    query = urllib.parse.urlparse(path).query
    if "=" in query:
        query_components = dict(qc.split("=") for qc in query.split("&"))
        for key in query_components:
            query_components[key] = urllib.parse.unquote_plus(query_components[key])
        #print(query_components["title"])
        if deletePost(query_components):
            return 204
        return 404

def handleRemoveUserApi(rawData):
    values = urllib.parse.parse_qs(rawData.decode("utf-8"))
    for key in values:
        values[key] = values[key][0]
    if ("username" in values.keys() and "password" in values.keys()):
        if (len(values["username"]) > 0 and len(values["password"]) > 0):
            if removeUser(values):
                return 200
            else:
                return 401
    return 400


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def checkForCookie(self):

        if(self.headers.get("Cookie")!=None):
            return True
        return False

    def end_headers(self):


        if(not self.checkForCookie()):
            c = generateSessionId()
            self.send_header('Set-Cookie', c.output(header=''))

        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        route=self.path.split("?")[0]

        if self.path == '/home.html':
            session=self.headers.get("Cookie")
            if(checkSession(session)):
                print("ok")
            else:
                self.send_response(401)
                self.path="/login.html"

        if self.path == '/addPost.html':
            session=self.headers.get("Cookie")
            if(checkSession(session)):
                print("ok")
            else:
                self.send_response(401)
                self.path="/login.html"



        print(self.path)
        if route == '/getPostsAPI':
            #getResource()
            #handleGet(self.path)

            content = handleGetPostsAPI(self.path)
            if content[0] == 200:
                self.send_response(content[0])
                self.send_header('Content-type', 'application/json')
                self.send_header('Location', '/posts')  # This will navigate to the original page
                self.end_headers()
                self.wfile.write(content[1])
            else:
                self.send_error(content[0])
            return
            #self.path = "/resource.txt"

        return http.server.SimpleHTTPRequestHandler.do_GET(self)


    def do_POST(self):
        if self.path == '/registerAPI':

            rawdata = self.rfile.read(int(self.headers['Content-Length']))
            response=handleRegisterApi(rawdata)
            if(response==201):
                self.send_response(response)
                self.end_headers()
                self.path="/login.html"
                self.do_GET()
            else:
                self.send_error(response)

        # if self.path == '/loginAPI':
        #     rawdata = self.rfile.read(int(self.headers['Content-Length']))
        #
        #     session=self.headers.get("Cookie")
        #     if(session==None):
        #         self.send_error(400)
        #     else:
        #         response=handleLoginApi(rawdata,session)
        #
        #         if(response==200):
        #             self.send_response(200)
        #             self.path="home.html"
        #             self.do_GET()
        #         else:
        #             self.send_error(response)

        if self.path == '/loginAPI':
            rawdata = self.rfile.read(int(self.headers['Content-Length']))

            session=6969
            if(session==None):
                self.send_error(400)
            else:
                response=handleLoginApi(rawdata,session)

                if(response==200):
                    self.send_response(200)
                    self.end_headers()
                    self.path="home.html"
                    self.do_GET()
                else:
                    self.send_error(response)

        # if self.path == '/addPostAPI':
        #     session = self.headers.get("Cookie")
        #     if (checkSession(session)):
        #         rawdata = self.rfile.read(int(self.headers['Content-Length']))
        #         response=handleAddPostAPI(rawdata,session)
        #         if (response == 201):
        #             self.send_response(201)
        #             self.path = "home.html"
        #             self.do_GET()
        #         else:
        #             self.send_error(response)
        #     else:
        #         self.send_response(401)
        #         self.path = "/login.html"

        if self.path == '/addPostAPI':
            #session = self.headers.get("Cookie")
            session=6969
            rawdata = self.rfile.read(int(self.headers['Content-Length']))
            #print("headers")
            #print(self.headers)
            #print("rawdata\n")

            #print(rawdata)
            response = handleAddPostAPI2(rawdata)
            if (response == 201):
                self.send_response(201)
                self.end_headers()
                self.path = "home.html"
                self.do_GET()
            else:
                self.send_error(response)

    def do_PUT(self):
        route = self.path.split("?")[0]
        if ("?" in self.path):
            args = self.path.split("?")[1]
        else:
            args = None

        if route=="/updatePostAPI":
            rawdata = self.rfile.read(int(self.headers['Content-Length']))
            #print(self.headers)
            #print(rawdata)
            self.send_error(handlePutAPI(rawdata))
            return

        if route=="/updatePasswordAPI":
            rawdata = self.rfile.read(int(self.headers['Content-Length']))
            #print(self.headers)
            #print(rawdata)
            response=handleChangePasswordAPI(rawdata);
            if(response==200):
                self.send_response(200)
                self.end_headers()
                return
            self.send_error(response)
            return


        self.send_error(404)

    def do_DELETE(self):
        route = self.path.split("?")[0]
        if("?" in self.path):
            args=self.path.split("?")[1]
        else:
            args=None


        if route=="/deletePostAPI":
            if args==None:
                self.send_error(400,"Missing Arguments")
                return
            else:
                response=handleDeleteAPI(self.path)
                if response<300:
                    self.send_error(response)
                    #self.send_response(response,"ok")
                    return
                else:
                    self.send_error(response)
                return

        if route == "/deleteUserAPI":
            rawdata = self.rfile.read(int(self.headers['Content-Length']))
            response = handleRemoveUserApi(rawdata)
            if(response==200):
                self.send_response(200)
                self.end_headers()
                return
            self.send_error(response)
            return

        self.send_error(404,"Api doesn't exist")




Handler = http.server.SimpleHTTPRequestHandler


def runServer():
    Handler = MyRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        httpd.serve_forever()


users=[]
openSessions=dict()
posts=dict()

loadPosts()
loadUsers()


runServer()
#getRandomPersonApi()
#generateImageApi()

