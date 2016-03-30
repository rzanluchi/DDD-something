from base import dispatcher
from base import event_store
from tab.repository import read_models
from tab.domain import aggregates


class Instance(object):

    def __init__(self):
        self.message_dispatcher = dispatcher.MessageDispatcher(
            event_store.InMemoryEventStore())
        self.chef_queries = read_models.ChefReadModel()
        self.tab_queries = read_models.OpenTabReadModel()

        # find a way to do this automatic
        self.message_dispatcher.add_handler_for(
            "open_tab", aggregates.TabAggregate)
        self.message_dispatcher.add_handler_for(
            "place_order", aggregates.TabAggregate)
        self.message_dispatcher.add_subscriber_for(
            "tab_opened", self.tab_queries)
        self.message_dispatcher.add_subscriber_for(
            "drinks_ordered", self.tab_queries)


instance = Instance()
