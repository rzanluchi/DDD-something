

class TabOpened(object):

    def __init__(self, id, table_number, waiter):
        self.event_name = "tab_opended"
        self.id = id
        self.table_number = table_number
        self.waiter = waiter
