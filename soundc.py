import soundcloud
import config


# LOG LOG LOG

class Sc:
    def __init__(self):
        self.client = soundcloud.Client(client_id=config.scId,
                                        client_secret=config.scSecret,
                                        username=config.scUsername,
                                        password=config.scPassword)

    def add(self, link, playlists):
        try:
            self.datas = self.client.get("/resolve", url=link)
        except:
            raise ValueError("Incorrect link: {}".format(link))
        if self.datas.kind == "track":
            self.addTrack(playlists)
        elif self.datas.kind == "playlist":
            self.client.put("/me/favorites/{}".format(self.datas.id))
        elif self.datas.kind == "user":
            self.client.put("/me/following/{}".format(self.datas.id))
        else:
            raise ValueError("Incorrect link: {}".format(link))
        return self.toDict()

    def addTrack(self, playlists):
        self.client.put("/me/favorites/{}".format(self.datas.id))
        for playlistName in playlists:
            playlistInfos = {'title': playlistName, 'sharing': "public"}
            playlist = self.client.post('/playlists', playlist=playlistInfos)
            track = {'tracks': map(lambda id: dict(id=id), [self.datas.id])}
            self.client.put(playlist.uri, playlist={'tracks': track})

    def toDict(self):
        dico = {}
        return dico


# create a client object with access token
client = soundcloud.Client(access_token='YOUR_ACCESS_TOKEN')

# create an array of track ids
tracks = map(lambda id: dict(id=id), [21778201, 22448500, 21928809])

# get playlist
playlist = client.get('/me/playlists')[0]

# add tracks to playlist
client.put(playlist.uri, playlist={
    'tracks': tracks
})
