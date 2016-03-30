

class ReadModel(object):

    def __init__(self):
        self.id = None
        self.events_loaded = 0

    def apply_events(self, events):
        for ev in events:
            if hasattr(self, "apply_{0}".format(ev.event_name)):
                func = getattr(self, "apply_{0}".format(ev.event_name))
                func(ev)
            else:
                raise Exception("Read Model {0} can't handle {1} event".format(
                                self, ev))
