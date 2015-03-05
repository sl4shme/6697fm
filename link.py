from datetime import datetime
import soundcloud_mgr
import youtube_mgr


class Link:
    def __init__(self, url, nick, playlist=None):
        self.url = self.sanitize(url)
        self.playlist = self.sanitize(playlist)
        self.date = datetime.now()
        self.nick = nick
        self.media = self.getMedia()
        self.infos = self.add()

    def sanitize(self, toClean):
        return toClean

    def getMedia(self):
        self.media = "soundcloud"

    def add(self):
        if self.media == "soundcloud":
            self.manager = soundcloud_mgr.Sc()
        if self.media == "youtube":
            self.manager = youtube_mgr.Sc()

        return self.manager.add(self.url, [self.nick, self.playlist])

    def toDict(self):
        data = {
                "url": self.url,
                "playlist": self.playlist,
                "date": self.date,
                "nick": self.nick,
                "media": self.media,
                "infos": self.infos
                }
        return data
