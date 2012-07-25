import bencode
from hashlib import sha1
import random
import urllib2
import urllib
from torrent.utils.url_fetcher import get_urls

# modified from http://nchachra.wordpress.com/2011/10/19/118/

def parse_torrent(torrent):
    ''' parse the torrent string and convert it to a dict '''
    decoded = bencode.bdecode(torrent)
    info = decoded['info']
    decoded_announce = decoded['announce']
    announce_list = [decoded_announce]
    try:
        announces = decoded['announce-list']
        for tracker in announces:
            if tracker != decoded_announce:
                announce_list.extend(tracker)
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
    try:
        response = urllib2.urlopen(url).read()
    except:
        return False
    return response


def get_peer_count(tracker,info_hash):
    # generate the peer_id
    rand_str = '-LT0160-'
    for i in range(12):
        rand_str = rand_str + chr(random.randint(0,255))
    peer_id = urllib.quote_plus(rand_str)
    info_hash = urllib.quote_plus(info_hash)

    url = ( tracker
          + "?info_hash="
          + info_hash
          + "&peer_id="
          + peer_id
          + "&port=9999&uploaded=0&downloaded=0&left=0&numwant=10&compact=1" )

    try:
        response = urllib2.urlopen(url).read()
    except:
        return False
    decoded_response = bencode.bdecode(response)
    try:
        decoded_response['complete']
    except:
        peer_count = decoded_response
    else:
        peer_count = {'tracker' : tracker,
            'seeders'  : decoded_response['complete'],
            'leachers' : decoded_response['incomplete'],
            'interval' : decoded_response['interval'],}
    return peer_count

def torrent_to_tracker_queries(torrent_info):
    ''' read torrent string. return the list of tracker URLs to query for info '''
    pass

def parse_tracker_responses(tracker_responses):
    ''' read list of tracker_responses, return parsed info '''
    pass

def get_tracker_info(torrent_info):
    tracker_queries = torrent_to_tracker_queries(torrent_info)
    tracker_responses = get_urls(tracker_queries)
    tracker_info = parse_tracker_responses(tracker_responses)
    return tracker_info

def get_torrent_info(torrent):
    parsed_torrent = parse_torrent(torrent)
    tracker_info = get_tracker_info(parsed_torrent)
    return {'tracker_info':tracker_info}
