from base import aggregate
from domain import events


class TabAggregate(aggregate.Aggregate):

    def handle_open_tab(self, command):
        return [events.TabOpened(command.id, command.table_number,
                                 command.waiter)]
