from base import dispatcher
from tab.repository import read_model


class Instance(object):

    def __init__(self):
        self.message_dispatcher = dispatcher.MessageDispatcher
        self.chef_queries = read_model.ChefReadModel()
        self.tab_queries = read_model.OpenTabReadModel()


instance = Instance()
