from . import listener

class KeepListener(listener.CommandListener):

    def __init__(self,core,counter):
        self.core = core
        self.counter = counter

    def command(self):
        return 'keep'

    def action(self, msg, user, channel):
        self.counter.add_keep(user)
        return 'Currently {} nexts and {} keeps'.format(len(self.counter.nexts),len(self.counter.keeps))

    def usage(self):
        return 'keep - Ask to keep the current playing song'
