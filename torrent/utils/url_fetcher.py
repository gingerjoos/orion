import threading
import urllib2
import Queue

class Fetcher(threading.Thread):

    def __init__(self,inQ,outQ):
        super(Fetcher,self).__init__()
        self.inQ = inQ
        self.outQ = outQ

    def run(self):
        print "starting to run " + self.getName()
        data = None
        try:
            url = self.inQ.get()
            print self.getName() + " starting to fetch URL : " + url
            response = urllib2.urlopen(url,None,10)
            data = response.read()
        except urllib2.URLError:
            print "URL Error"
        except urllib2.HTTPError:
            print "HTTP Error"

        qData = {'url':url,'data':data}
        self.outQ.put(qData)
        self.inQ.task_done()

def get_urls(urls):
    no_of_urls = len(urls)
    # TODO : spawn no_of_urls no. of Fetchers
    # TODO : insert into queue
    # TODO : read from queue

inQ = Queue.Queue()
outQ = Queue.Queue()

urls = ['https://api.twitter.com/1/statuses/user_timeline.json?screen_name=gingerjoos&include_rts=true','http://pipes.yahoo.com/pipes/pipes.popular?_out=json']
for i in range(2):
    fetcher = Fetcher(inQ,outQ)
    fetcher.setDaemon(True)
    fetcher.start()

for url in urls:
    inQ.put(url)

inQ.join()
for i in range(2):
    print outQ.get()
    outQ.task_done()
#outQ.join()

#print outQ
