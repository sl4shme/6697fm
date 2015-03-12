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
    newLink = link.Link(url, msg['to']['print_name'], hashtags)
    entry = newLink.toDict()
    entry['msg'] = msg
    db = tddb.TinyDictDb(config.linkDb)
    db.addEntries(entry)
    if entry['infos']['media'] == "youtube":
        if entry['infos']['kind'] == "track":
            resp = "Added this track to my channel https://www.youtu.be/channel/UC-6seI5JtZV8tKCapPo_j_A/feed on playlists: {}".format(str(entry['playlists']))
        else:
            resp = "Youtube doesn't know how to deal with user and playlists, still logging for posterity."

    if entry['infos']['media'] == "soundcloud":
        resp = "Added this {} to my account https://soundcloud.com/6697Fm".format(entry['infos']['kind'])
        if entry['infos']['kind'] == "track":
            resp += " on playlists : {}".format(str(entry['playlists']))
    print(resp)
except:
    sys.exit(1)
