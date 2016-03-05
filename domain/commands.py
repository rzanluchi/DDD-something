

class OpenTab(object):

    def __init__(self, id, table_number, waiter):
        self.command_name = "open_tab"
        self.id = id
        self.table_number = table_number
        self.waiter = waiter
