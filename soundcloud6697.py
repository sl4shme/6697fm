import soundcloud
import config


class Sc:
    def __init__(self):
        self.client = soundcloud.Client(client_id=config.scId,
                                        client_secret=config.scSecret,
                                        username=config.scUsername,
                                        password=config.scPassword)

    def connect(self):
        pass

    def check(self, link):
        try:
            self.datas = self.client.get("/resolve", url=link)
        except:
            raise ValueError("Incorrect link: {}".format(link))
        return self.datas.permalink_url

    def add(self, playlists):
        if self.datas.kind == "track":
            self.addTrack(playlists)
        elif self.datas.kind == "playlist":
#            self.client.put("/me/favorites/{}".format(self.datas.id))
            pass
        elif self.datas.kind == "user":
            self.client.put("/me/followings/{}".format(self.datas.id))
        else:
            raise ValueError("Link not track, playlist or user.")
        return self.toDict()

    def addTrack(self, playlists):
        self.client.put("/me/favorites/{}".format(self.datas.id))
        myplaylist = self.client.get('/me/playlists')
        for playlistName in playlists:
            if playlistName in [item.title for item in myplaylist]:
                infos = [item for item in myplaylist if item.title ==
                         playlistName][0]
                uri = infos.uri
                tracks = [{'id': item['id']} for item in infos.tracks]
                tracks.append({'id': self.datas.id})
                tracks = {'tracks': tracks}
            else:
                playlistInfos = {'title': playlistName, 'sharing': "public"}
                playlist = self.client.post('/playlists',
                                            playlist=playlistInfos)
                uri = playlist.uri
                tracks = {'tracks': [{'id': self.datas.id}]}
            self.client.put(uri, playlist=tracks)

    def toDict(self):
        dico = {'media': "soundcloud",
                'kind': self.datas.kind,
                'uri': self.datas.uri}
        if self.datas.kind == "user":
            dico['full_name'] = self.datas.full_name
            dico['username'] = self.datas.username
        else:
            dico['title'] = self.datas.user['username']+" - "+self.datas.title
        return dico
