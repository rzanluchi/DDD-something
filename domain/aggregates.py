from base import aggregate
from domain import events
from domain import exceptions


class TabAggregate(aggregate.Aggregate):

    def __init__(self):
        super(TabAggregate, self).__init__()
        self.opened = False

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

    def apply_tab_opended(self, event):
        self.opened = True
