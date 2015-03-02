import soundcloud
import config


class Sc:
    def __init__(self):
        self.client = soundcloud.Client(client_id=config.scId,
                                        client_secret=config.scSecret,
                                        username=config.scUsername,
                                        password=config.scPassword)

    def checkLink(self, link):
        self.client.get("/resolve", url="https://soundcloud.com/"
                                        "gotmyboysinthewater/princes-1")

    def addToPlaylist(self, playlist, link):
        pass
