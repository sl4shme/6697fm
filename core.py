import tinydictdb as tddb
import json
import sys
import re
import link
import config

msg = json.loads(sys.argv[1])
url = re.search("(?P<url>https?://[^\s]+)", msg['text']).group("url")
hashtags = [word[1:] for word in msg['text'].split() if word[0] == '#']
hashtags = list(set(hashtags))

try:
    newLink = link.Link(url, msg['from']['print_name'], hashtags)
    entry = newLink.toDict()
    entry['msg'] = msg
    db = tddb.TinyDictDb(config.linkDb)
    db.addEntries(entry)
    if entry['infos']['kind'] == "track":
        entry['playlists'].append("favorites")
    if entry['infos']['media'] == "youtube":
        if entry['infos']['kind'] == "track":
            resp = "Added this track to my channel http://bit.ly/19ekX3p on playlists: {}".format(str(entry['playlists']))
        else:
            resp = "Youtube doesn't know how to deal with user and playlists, still logging for posterity."
    
    if entry['infos']['media'] == "soundcloud":
        resp = "Added this {} to my account http://bit.ly/1wZuyFT".format(entry['infos']['kind'])
        if entry['infos']['kind'] == "track":
            resp += " on playlists : {}".format(str(entry['playlists']))
        if entry['infos']['kind'] == "playlist":
            resp = "Soundcloud doesn't support liking playlists using the api. Still logging for posterity."
    print(resp)
except:
    sys.exit(1)
