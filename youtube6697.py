import gdata.youtube
import gdata.youtube.service
import config
import urllib2
import lxml.etree


class Yt:
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
                channelName = [i.attrib['content'] for i in meta if
                               i.attrib['itemprop'] == "name"]
                self.resTitle = channelName[0]
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
            print("Playlists are not supported for now.")
        elif self.kind == "playlist":
            uri = "http://gdata.youtube.com/feeds/api/playlists/"+self.resId
            playlist = self.client.GetYouTubePlaylistVideoFeed(uri=uri)
            self.resTitle = playlist.title.text
            print("Playlists are not supported for now.")
        else:
            raise ValueError("Link not track, user or playlist.")
        return self.toDict()

    def addTrack(self, playlistNames):
        video = self.client.GetYouTubeVideoEntry(video_id=self.resId)
        resp = self.client.AddVideoEntryToFavorites(video)
        if isinstance(resp, gdata.youtube.YouTubeVideoEntry):
            self.resTitle = resp.title.text
        else:
            raise ValueError("Error when liking sound.")

        playlists = self.getPlaylists()
        for playlistName in playlistNames:
            if any(i['title'] == playlistName for i in playlists):
                uri = [i['id'] for i in playlists if i['title'] ==
                       playlistName][0]
                new = False
            else:
                resp = self.client.AddPlaylist(playlistName, playlistName)
                if isinstance(resp, gdata.youtube.YouTubePlaylistEntry):
                    uri = resp.FindExtensions("playlistId")[0].text
                    new = True
                else:
                    raise ValueError("Failed to create playlist.")
            uri = "http://gdata.youtube.com/feeds/api/playlists/"+uri

            if not new and (self.resTitle in self.getPlaylist(uri)):
                print("Video already present in playlist.")
            else:
                resp = self.client.AddPlaylistVideoEntryToPlaylist(uri,
                                                                   self.resId)
                if not isinstance(resp,
                                  gdata.youtube.YouTubePlaylistVideoEntry):
                    raise ValueError('Failed to add video to playlist.')

    def getPlaylists(self):
        playlist_feed = self.client.GetYouTubePlaylistFeed(username='default')
        playlists = []
        for entry in playlist_feed.entry:
            pId = entry.FindExtensions("playlistId")[0].text
            title = entry.title.text
            playlists.append({"id": pId, "title": title})
        return playlists

    def getPlaylist(self, uri):
        playlist = self.client.GetYouTubePlaylistVideoFeed(uri=uri)
        titles = []
        for video in playlist.entry:
            titles.append(video.title.text)
        return titles

    def toDict(self):
        dico = {'media': "youtube",
                'kind': self.kind,
                'id': self.resId,
                'title': self.resTitle}
        return dico
