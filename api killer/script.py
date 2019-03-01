import urllib.request
import time
import threading

def sendRequest(url):
    start=time.time()
    response=urllib.request.urlopen(url)
    content=response.read()
    return  time.time()-start

def monitor(reqNum,index,url):
    # req = urllib.request.Request(
    #     url,
    #     data=None,
    #     headers={
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    #     }
    # )
    # urllib.request.urlopen(req)
    reqNum[index]=sendRequest(url)
    #reqNum[index] = time.time()


def getAliveCount(threads):
    count=0
    for thread in threads:
        if thread.is_alive():
            count+=1
    return count

def doNothing(a,b,c):
    print(b)
def problema(url):
    reqNum=[None]*50
    thread=[]
    for i in range(0,50):
        thread.append( threading.Thread(target = monitor, args = (reqNum,i,url)))
    for i in range(0, 5):
        thread[i].start()

    #     #thread.join()
    #     #for i in range(0, 50):
    #      #   thread[i].join()
    while getAliveCount(thread)>0:
        time.sleep(1)
    print(reqNum)

problema("http://localhost:8000/getRandomPerson")
#sendRequest("http://localhost:44355/page.html")

#sendRequest("http://localhost:8000/getRandomPerson")