

class Aggregate(object):

    def __init__(self):
        self.id = None
        self.events_loaded = 0

    def apply_events(self, events):
        for ev in events:
            if hasattr(self, "apply_{0}".format(ev.event_name)):
                func = getattr(self, "apply_{0}".format(ev.event_name))
                func(ev)
            else:
                raise Exception("Aggregate {0} can't handle {1} event".format(
                                self, ev))

    def handle(self, command):
        if hasattr(self, "handle_{0}".format(command.command_name)):
            func = getattr(self, "handle_{0}".format(command.command_name))
            return func(command)
        else:
            raise Exception("Aggregate {0} can't handle {1} command".format(
                            self, command))
