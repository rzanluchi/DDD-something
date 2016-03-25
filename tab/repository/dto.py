class ChefListItemDTO(object):

    def __init__(self, item_id, description):
        self.item_id = item_id
        self.description = description


class ChefListGroupDTO(object):

    def __init__(self, tab_id, items):
        self.tab_id = tab_id
        self.items = items


class TabDTO(object):

    def __init__(self, table_number, waiter, items_to_serve, served_items):
        self.table_number = table_number
        self.waiter = waiter
        self.items_to_serve = items_to_serve
        self.served_items = served_items
