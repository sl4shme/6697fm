import gdata.youtube
import gdata.youtube.service
import config
import urllib2
import lxml.etree

class Sc:
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.yt_service.ssl = True
        self.yt_service.developer_key = config.ytDevelopperKey
        self.yt_service.client_id = config.ytClientId
        self.yt_service.source = config.ytClientId
        self.yt_service.email = config.ytEmail
        self.yt_service.password = config.ytPassword
        self.yt_service.ProgrammaticLogin()

    def check(self, link):
        page = urllib2.urlopen(link)
        finalUrl = page.geturl()
        content = page.read()
        page.close()
        tree = lxml.etree.HTML(content)
        meta = tree.xpath("//meta[@itemprop]")
        videoId = [i.attrib['content'] for i in c if i.attrib['itemprop'] ==
                     "videoId"][0]
        if videoId:
            self.kind = "track"
            self.resId = videoId
        else:
            channelId = [i.attrib['content'] for i in c if i.attrib['itemprop']
                         == "channelId"][0]
            if channelId:
                self.kind = "user"
                self.resId = channelId
            else:
                div = tree.xpath("//div[@data-playlist-id]")







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
            dico['title'] = self.datas.title
        return dico

    data-playlist-id=""
