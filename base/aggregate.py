

class Aggregate(object):

    def __init__(self):
        self.id = None
        self.events_loaded = 0

    def apply_events(self, events):
        pass

    def handle(self, command):
        if hasattr(self, "handle_{0}".format(command.command_name)):
            func = getattr(self, "handle_{0}".format(command.command_name))
            return func(command)
        else:
            return None
