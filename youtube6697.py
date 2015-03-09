import gdata.youtube
import gdata.youtube.service
import config
import urllib2
import lxml.etree


class Yt:
    def __init__(self):
        pass

    def connect(self):
        self.client = gdata.youtube.service.YouTubeService()
        self.client.ssl = True
        self.client.developer_key = config.ytDevelopperKey
        self.client.client_id = config.ytClientId
        self.client.source = config.ytClientId
        self.client.email = config.ytEmail
        self.client.password = config.ytPassword
        self.client.ProgrammaticLogin()

    def check(self, link):
        page = urllib2.urlopen(link)
        self.finalUrl = page.geturl()
        content = page.read()
        page.close()
        tree = lxml.etree.HTML(content)
        meta = tree.xpath("//meta[@itemprop]")
        videoId = [i.attrib['content'] for i in meta if i.attrib['itemprop'] ==
                   "videoId"]
        if videoId:
            self.kind = "track"
            self.resId = videoId[0]
        else:
            channelId = [i.attrib['content'] for i in meta if
                         i.attrib['itemprop'] == "channelId"]
            if channelId:
                self.kind = "user"
                self.resId = channelId[0]
            else:
                div = tree.xpath("//div[@data-playlist-id]")
                playlistId = [i.attrib['data-playlist-id'] for i in div]
                if playlistId:
                    self.kind = "playlist"
                    self.resId = playlistId[0]
                else:
                    raise ValueError("Invalid link.")
            return self.finalUrl

    def add(self, playlists):
        self.connect()
        if self.kind == "track":
            self.addTrack(playlists)
        elif self.kind == "user":
            self.client.put("/me/following/{}".format(self.datas.id))
        elif self.kind == "playlist":
            print("Playlists are not supported for now.") 
        else:
            raise ValueError("Link not track, user or playlist.")
        return self.toDict()

    def addTrack(self, playlists):
        video = self.client.GetYouTubeVideoEntry(video_id=self.resId)
        resp = self.client.AddVideoEntryToFavorites(video)
        if not isinstance(resp, gdata.youtube.YouTubeVideoEntry):
            raise ValueError("Error liking sound.")
        plists = yt_service.GetYouTubePlaylistFeed(username=config.ytUsername)

        for playlistName in playlists:
            playlist_feed =
            p = yt_service.AddPlaylist(playlistName,playlistName)
            if isinstance(p, gdata.youtube.YouTubePlaylistEntry):
      print 'New playlist added'

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
