

class InMemoryEventStore(object):

    def __init__(self):
        # a dict by aggregate name and aggregate id
        self.memory = {}

    def store(self, aggregate, events):
        if aggregate.name not in self.memory.keys():
            self.memory[aggregate.name] = {}

        for event in events:
            if event.id not in self.memory[aggregate.name]:
                self.memory[aggregate.name][event.id] = [event]
            else:
                self.memory[aggregate.name][event.id].append(event)

    def load(self, aggregate, id):
        ag = self.memory.get(aggregate.name)
        if ag:
            return ag.get(id, [])
        else:
            return []
