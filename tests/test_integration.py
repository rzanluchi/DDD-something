from instance import Instance
from tab.domain import commands, events


class TestInstanceIntegrationAggregateReadModel(object):

    def setup_method(self, method):
        self.instance = Instance()

    def test_open_tab_command_should_update_read_model(self):
        assert self.instance.tab_queries.active_table_numbers() == []
        open_tab = commands.OpenTab(190, 27, "jose")
        self.instance.message_dispatcher.publish_command(open_tab)
        assert 27 in self.instance.tab_queries.active_table_numbers()

    def test_place_order_should_have_items_to_serve_at_tab_dto(self):
        open_tab = commands.OpenTab(190, 27, "jose")
        self.instance.message_dispatcher.publish_command(open_tab)
        place_order = commands.PlaceOrder(190, [
            events.OrderedItem(44, "Coke", 1.50, True)
        ])
        self.instance.message_dispatcher.publish_command(place_order)
        jose_todo = self.instance.tab_queries.todo_list_for_waiter('jose')
        assert len(jose_todo) == 1
        assert jose_todo[0].items_to_serve[0].menu_number== 44
        assert jose_todo[0].items_to_serve[0].description == "Coke"
