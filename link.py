from datetime import datetime


class Link:
    def __init__(self, url, tag, pseudo):
        self.url = url
        self.tags = tag
        self.date = datetime.now()
        self.pseudo = pseudo
        self.sourceType = self.getSourceType(self.url)
        self.name = self.getInfos(self.url, self.sourceType)

    def getSourceType(self, url):
        pass

    def getInfos(self, url, sourceType):
        pass

    def toDict(self):
        pass
