

class TestDriver(object):

    def __init__(self, aggregate):
        self.aggregate = aggregate

    def given(self, events=[]):
        self.apply_events(self.aggregate, events)
        return self

    def when(self, command):
        self.events = self.aggregate.handle(command)
        if not self.events:
            raise Exception("Aggregate {0} can't handle {1} command".format(
                            self.aggregate, command))
        return self

    def then(self, expected_events=[]):
        if len(self.events) == len(expected_events):
            for i in range(len(self.events)):
                assert self.compare(self.events[i], expected_events[i])
        else:
            # this will trigger assertion error
            assert self.events == expected_events

    def apply_events(self, aggregate, events):
        if events:
            aggregate.apply_events(events)

    def compare(self, target_event, expected_event):
        raise Exception("You need to overwrite the compare method")
