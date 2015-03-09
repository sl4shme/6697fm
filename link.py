from datetime import datetime
import soundcloud6697
import youtube6697


class Link:
    def __init__(self, url, nick, playlist=None):
        self.url = self.sanitize(url)
        self.playlist = self.sanitize(playlist)
        self.date = datetime.now()
        self.nick = self.sanitize(nick)
        self.infos = self.add()

    def sanitize(self, toClean):
        return str(toClean)

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
            return self.manager.add([self.nick, self.playlist])

    def toDict(self):
        data = {
                "url": self.url,
                "playlist": self.playlist,
                "date": self.date,
                "nick": self.nick,
                "infos": self.infos
                }
        return data
