from threading import Timer
from . import listener

class NextListener(listener.CommandListener):

    def __init__(self,core,counter):
        self.core = core
        self.counter = counter

    def command(self):
        return 'next'

    def action(self, msg, user, channel):
        if len(self.counter.nexts) == 0:
            Timer(15.0,self.change_song).start()
            self.counter.add_next(user)
            return 'In 10 seconds song will be next'

        self.counter.add_next(user)
        return 'Currently {} nexts and {} keeps'.format(len(self.counter.nexts),len(self.counter.keeps))

    def usage(self):
        return 'next - Ask to skip the current playing song'

    def change_song(self):
        if len(self.counter.nexts) > len(self.counter.keeps):
            self.core.playback.next()

class NextCounter():

    def __init__(self):
        self.reset()

    def add_next(self,user):
        self.nexts.add(user)

    def add_keep(self,user):
        self.keeps.add(user)

    def reset(self):
        self.nexts = set()
        self.keeps = set()

