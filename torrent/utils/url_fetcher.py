import threading
import urllib2
import Queue

class ThreadedFetcher(threading.Thread):

    def __init__(self,inQ,outQ):
        super(ThreadedFetcher,self).__init__()
        self.inQ = inQ
        self.outQ = outQ

    def run(self):
        print "starting to run " + self.getName()
        url = self.inQ.get()
        single_fetcher = SingleFetcher(url)
        qData = single_fetcher.run()
        self.outQ.put(qData)
        self.inQ.task_done()

class SingleFetcher():

    def __init__(self,url):
        self.url = url

    error = True
    def run(self):
        try:
            response = urllib2.urlopen(self.url,None,10)
            data = response.read()
        except urllib2.URLError:
            error = True
        except urllib2.HTTPError:
            error = True

        qData = {'url':self.url,'text':data,'error':error}

class Fetcher():
    def start(url):
        pass

#inQ = Queue.Queue()
#outQ = Queue.Queue()
#
#for i in range(2):
#    fetcher = ThreadedFetcher(inQ,outQ)
#    fetcher.setDaemon(True)
#    fetcher.start()
#
#for url in urls:
#    inQ.put(url)
#
#inQ.join()
#for i in range(2):
#    print outQ.get()
#    outQ.task_done()
##outQ.join()
#
##print outQ

def get_urls(urls):
    no_of_urls = len(urls)
    inQ = Queue.Queue()
    outQ = Queue.Queue()
    results = []

    # spawn the reqd no. of ThreadedFetcher threads
    for i in range(no_of_urls):
        fetcher = ThreadedFetcher(inQ,outQ)
        fetcher.setDaemon(True)
        fetcher.start()
    # insert into the IN Queue
    for url in urls:
        inQ.put(url)

    # wait for IN Queue
    inQ.join()

    # get the result from the OUT Queue
    for i in range(no_of_urls):
        response = outQ.get()
        outQ.task_done()
        result.append(response)

    return result
