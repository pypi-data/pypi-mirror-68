import logging

from ..utils import title_dash_artist
from . import listener

logger = logging.getLogger(__name__)

class RequestListener(listener.CommandListener):

    def __init__(self,core):
        self.core = core

    def command(self):
        return 'request'

    def action(self, msg, user, channel):
        split = msg[8:].strip().split('-')

        if len(split) == 1:
            query = {'any': split[0].strip().split(' ')}
        else:
            query = {'track_name': split[0].strip().split(' '),
                     'artist': split[1].strip().split(' ')}

        results = self.core.library.search(query).get()
        source = results[0]
        logger.info('{} results matching query {} and uri {}'.format(len(source.tracks), query, source.uri))
        if len(source.tracks) <= 0:
            return 'Nothing match your query :('
        else:
            next_track = source.tracks[0]
            current_track_position = self.core.tracklist.index().get()
            current_track_position = -1 if current_track_position is None else current_track_position
            logger.info('current position {}'.format(current_track_position))
            self.core.tracklist.add(tracks=[next_track],
                                    at_position=current_track_position + 1)
            return 'Coming next {}'.format(title_dash_artist(next_track))

    def usage(self):
        return 'request song_name [- artist_name] - Request a new song to be played'

