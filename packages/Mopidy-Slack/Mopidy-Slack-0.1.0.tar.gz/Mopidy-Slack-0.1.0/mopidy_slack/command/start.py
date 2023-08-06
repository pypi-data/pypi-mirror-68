from . import listener
import random

class StartListener(listener.CommandListener):

    def __init__(self,core, channel_holder):
        self.core = core
        self.started = False
        self.channel_holder = channel_holder

    def command(self):
        return 'start'

    def action(self, msg, user, channel):
        if self.started:
            return 'Already started'

        query = msg[6:]
        playlist = self.find_playlist(query)
        if playlist is None:
            return "Couldn't find playlist name starting by {}".format(query)
        self.core.tracklist.add(uris=[playlist.uri])
        self.core.tracklist.shuffle()
        self.core.playback.play()
        self.started = True
        self.channel_holder.set_channel(channel)
        return 'On air with {}'.format(playlist.name)

    def usage(self):
        return 'start [playlist_name] - Start the radio broadcast'

    # Search for an existing playlist starting with query
    # Otherwise return the default playlist
    def find_playlist(self, query):
        playlists = self.core.playlists.as_list().get()
        if query == "":
            playlists[random.randint(0,len(playlists))]
        for playlist in playlists:
            if playlist is not None and playlist.name.lower().startswith(query.lower()):
                return playlist
        return None
