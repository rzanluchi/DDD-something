from base import aggregate
from domain import events
from domain import exceptions


class TabAggregate(aggregate.Aggregate):

    def __init__(self):
        super(TabAggregate, self).__init__()
        self.opened = False
        self.outstanding_drinks = []

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

    def apply_tab_opended(self, event):
        self.opened = True

    def apply_drinks_ordered(self, event):
        self.outstanding_drinks += event.items

    def apply_drinks_served(self, event):
        def _filter(drink):
            return drink.id not in event.item_ids
        self.outstanding_drinks = filter(_filter, self.outstanding_drinks)

    def _are_drinks_outstanding(self, item_ids):
        outstanding_ids = [item.id for item in self.outstanding_drinks]
        for item_id in item_ids:
            if item_id not in outstanding_ids:
                return False

        return True
