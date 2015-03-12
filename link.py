from datetime import datetime
import soundcloud6697
import youtube6697
import re


class Link:
    def __init__(self, url, nick, playlists=[]):
        self.url = self.sanitize(url)
        self.playlists = self.sanitize(playlists)
        self.date = datetime.now()
        self.nick = self.sanitize(nick)
        self.infos = self.add()

    def sanitize(self, toClean):
        if type(toClean) == list:
            cleaned = []
            for i in toClean:
                clean = self.sanitize(i)
                cleaned.append(clean)
            return cleaned
        toClean = str(toClean)
        toClean = toClean.lower()
        toClean = re.sub("[^a-z0-9]", "_", toClean)
        toClean = re.sub("_+", "_", toClean)
        return toClean

    def add(self):
        scFailed = False
        ytFailed = False
        okay = False
        if "soundcloud" in self.url:
            try:
                self.manager = soundcloud6697.Sc()
                self.url = self.manager.check(self.url)
                okay = True
            except:
                scFailed = True
        elif "youtu" in self.url:
            try:
                self.manager = youtube6697.Yt()
                self.url = self.manager.check(self.url)
                okay = True
            except:
                ytFailed = True
        if not okay:
            try:
                if scFailed:
                    raise ValueError("dummie")
                self.manager = soundcloud6697.Sc()
                self.url = self.manager.check(self.url)
                okay = True
            except:
                try:
                    if ytFailed:
                        raise ValueError("dummie")
                    self.manager = youtube6697.Yt()
                    self.url = self.manager.check(self.url)
                    okay = True
                except:
                    raise ValueError("Link not valid.")
        if okay:
            self.manager.connect()
            self.playlists.append(self.nick)
            return self.manager.add(self.playlists)

    def toDict(self):
        data = {
                "url": self.url,
                "playlists": self.playlists,
                "date": self.date,
                "nick": self.nick,
                "infos": self.infos
                }
        return data
