import threading
import urllib2
import Queue

class Fetcher(threading.Thread):

    def __init__(self,queue,out_queue):
        super(Fetcher,self).__init__()
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        print self.getName()
        try:
            url = self.queue.get()
            response = urllib2.urlopen(url)
            data = response.read()
        except urllib2.URLError:
            pass
        except urllib2.HTTPError:
            pass
