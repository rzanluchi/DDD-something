

class OpenTab(object):

    def __init__(self, id, table_number, waiter):
        self.command_name = "open_tab"
        self.id = id
        self.table_number = table_number
        self.waiter = waiter


class PlaceOrder(object):

    def __init__(self, id, items):
        self.command_name = "place_order"
        self.id = id
        self.items = items


class MarkDrinksServed(object):

    def __init__(self, id, item_ids):
        self.command_name = "mark_drinks_served"
        self.id = id
        self.item_ids = item_ids


class CloseTab(object):

    def __init__(self, id, amount_paid):
        self.command_name = 'close_tab'
        self.id = id
        self.amount_paid = amount_paid
