

class ReadModel(object):

    def __init__(self):
        self.id = None
        self.events_loaded = 0

    def apply(self, event):
        if hasattr(self, "apply_{0}".format(event.event_name)):
            func = getattr(self, "apply_{0}".format(event.event_name))
            func(event)
        else:
            raise Exception("Read Model {0} can't handle {1} event".format(
                            self, event))
