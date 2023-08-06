import pykka
from mopidy.core import CoreListener
from .utils import title_dash_artist

class SongNotification(pykka.ThreadingActor, CoreListener):

    def __init__(self, slack_connector, next_counter, channel_holder):
        super(SongNotification, self).__init__()
        self.slack_connector = slack_connector
        self.next_counter = next_counter
        self.channel_holder = channel_holder
        self.channel = ""

    def track_playback_started(self, tl_track):
        current_track = tl_track.track
        current_track = "None" if current_track is None else title_dash_artist(current_track)
        self.slack_connector.send_message(body=current_track, channel=self.channel_holder.get_channel())
        self.next_counter.reset()

