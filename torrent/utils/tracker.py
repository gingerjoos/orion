import bencode
from hashlib import sha1
import random
import urllib2
import urllib

# modified from http://nchachra.wordpress.com/2011/10/19/118/

def parse_torrent(torrent):
    decoded = bencode.bdecode(torrent)
    info = decoded['info']
    decoded_announce = decoded['announce']
    announce_list = [decoded_announce]
    try:
        announces = decoded['announce-list']
        announce_list.extend(announces)
    except:
        pass
    encoded_info = bencode.bencode(info)
    info_digest = sha1(encoded_info).digest()
    #info_hash = urllib.quote_plus(info_digest)

    decoded['info_hash'] = info_digest
    decoded['trackers'] = announce_list
    return decoded

def read_torrent_file(filename):
    fileh = open(filename,'rb')
    torrent = fileh.read()
    fileh.close()
    return torrent

def read_torrent_url(url):
    response = urllib2.urlopen(url).read()
    return response


def get_peer_count(tracker,info_hash):
    # generate the peer_id
    rand_str = '-LT0160-'
    for i in range(12):
        rand_str = rand_str + chr(random.randint(0,255))
    peer_id = urllib.quote_plus(rand_str)

    url = tracker + "?info_hash=" + info_hash + "&peer_id=" + peer_id + "&port=9999&uploaded=0&downloaded=0&left=0&numwant=10&compact=1"

    response = urllib2.urlopen(url).read()
    decoded_response = bencode.bdecode(response)

    peer_count = {'seeders'  : decoded_response['complete'],
            'leachers' : decoded_response['incomplete'],
            'interval' : decoded_response['interval'],}
    return peer_count

def get_tracker_info(torrent):
    torrent_info = parse_torrent(torrent)
    trackers = torrent_info['trackers']
    tracker_info = []
    for tracker in trackers:
        tracker_info.append(get_peer_count(tracker,torrent_info['info_hash']))
    return tracker_info