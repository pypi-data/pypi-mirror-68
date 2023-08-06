import logging

def title_dash_artist(track):
    if len(track.artists) < 1:
        return track.name
    return track.name + " - " + next(iter(track.artists)).name

