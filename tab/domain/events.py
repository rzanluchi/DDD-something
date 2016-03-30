class TabOpened(object):

    def __init__(self, id, table_number, waiter):
        self.event_name = 'tab_opened'
        self.id = id
        self.table_number = table_number
        self.waiter = waiter


class OrderedItem(object):

    def __init__(self, menu_number, description, price, is_drink):
        self.event_name = 'ordered_item'
        self.menu_number = menu_number
        self.description = description
        self.price = price
        self.is_drink = is_drink


class DrinksOrdered(object):

    def __init__(self, id, items):
        self.event_name = 'drinks_ordered'
        self.id = id
        self.items = items


class FoodOrdered(object):

    def __init__(self, id, items):
        self.event_name = 'food_ordered'
        self.id = id
        self.items = items


class DrinksServed(object):

    def __init__(self, id, item_ids):
        self.event_name = 'drinks_served'
        self.id = id
        self.item_ids = item_ids


class FoodServed(object):

    def __init__(self, id, item_ids):
        self.event_name = 'food_served'
        self.id = id
        self.item_ids = item_ids


class TabClosed(object):

    def __init__(self, id, amount_paid, order_value, tip_value):
        self.event_name = 'tab_closed'
        self.id = id
        self.amount_paid = amount_paid
        self.order_value = order_value
        self.tip_value = tip_value
