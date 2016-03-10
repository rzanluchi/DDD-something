from base import aggregate
from domain import events
from domain import exceptions


class TabAggregate(aggregate.Aggregate):

    def __init__(self):
        super(TabAggregate, self).__init__()
        self.opened = False
        self.outstanding_drinks = []
        self.outstanding_food = []
        self.served_items_value = 0

    def handle_open_tab(self, command):
        return [events.TabOpened(command.id, command.table_number,
                                 command.waiter)]

    def handle_place_order(self, command):
        if not self.opened:
            raise exceptions.TabNotOpen("Can't open a unopen tab")

        return_events = []
        drinks = [drink for drink in command.items if drink.is_drink]
        if any(drinks):
            return_events.append(
                events.DrinksOrdered(id=command.id, items=drinks))

        foods = [food for food in command.items if not food.is_drink]
        if any(foods):
            return_events.append(events.FoodOrdered(id=command.id, items=foods))

        return return_events

    def handle_mark_drinks_served(self, command):
        if not self._are_drinks_outstanding(command.item_ids):
            raise exceptions.DrinksNotOutstanding
        return [events.DrinksServed(id=command.id,
                                    item_ids=command.item_ids)]

    def handle_mark_food_served(self, command):
        if not self._are_food_outstanding(command.item_ids):
            raise exceptions.FoodNotOutstanding
        return [events.FoodServed(id=command.id, item_ids=command.item_ids)]

    def handle_close_tab(self, command):
        if command.amount_paid < self.served_items_value:
            raise exceptions.MustPayEnough
        if not self.opened:
            raise exceptions.TabNotOpen
        if self.outstanding_drinks:
            raise exceptions.DrinksUnserved
        if self.outstanding_food:
            raise exceptions.FoodUnserved

        return [events.TabClosed(
            id=command.id, amount_paid=command.amount_paid,
            order_value=self.served_items_value,
            tip_value=command.amount_paid - self.served_items_value)
        ]

    def apply_tab_opended(self, event):
        self.opened = True

    def apply_drinks_ordered(self, event):
        self.outstanding_drinks += event.items

    def apply_food_ordered(self, event):
        self.outstanding_food += event.items

    def apply_drinks_served(self, event):
        new_list = []
        for drink in self.outstanding_drinks:
            if drink.id in event.item_ids:
                self.served_items_value += drink.price
            else:
                new_list.append(drink)
        self.outstanding_drinks = new_list

    def apply_food_served(self, event):
        new_list = []
        for food in self.outstanding_food:
            if food.id in event.item_ids:
                self.served_items_value += food.price
            else:
                new_list.append(food)
        self.outstanding_food = new_list

    def apply_tab_closed(self, event):
        self.opened = False
        self.served_items_value = 0

    def _are_drinks_outstanding(self, item_ids):
        outstanding_ids = [item.id for item in self.outstanding_drinks]
        for item_id in item_ids:
            if item_id not in outstanding_ids:
                return False

        return True

    def _are_food_outstanding(self, item_ids):
        outstanding_ids = [item.id for item in self.outstanding_food]
        for item_id in item_ids:
            if item_id not in outstanding_ids:
                return False

        return True
