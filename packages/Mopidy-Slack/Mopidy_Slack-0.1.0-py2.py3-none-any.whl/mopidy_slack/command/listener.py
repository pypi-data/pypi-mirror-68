from abc import abstractmethod

class CommandListener():

    @abstractmethod
    def command(self):
        pass

    @abstractmethod
    def action(self, msg, user, channel):
        pass

    @abstractmethod
    def usage(self):
        pass