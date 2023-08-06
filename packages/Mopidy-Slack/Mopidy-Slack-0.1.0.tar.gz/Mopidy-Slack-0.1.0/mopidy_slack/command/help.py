from . import listener

class HelpListener(listener.CommandListener):

    def __init__(self, listeners):
        self.listeners = listeners

    def command(self):
        return 'help'

    def action(self, msg, user, channel):
        usage =''
        for listener in self.listeners:
            usage += listener.usage() + '\n'
        return usage

    def usage(self):
        return 'help - Display this help'