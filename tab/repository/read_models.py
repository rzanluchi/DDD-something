from base import read_model
from tab.repository import dto


class ChefReadModel(read_model.ReadModel):

    def __init__(self):
        self.item_groups = []

    def get_todo_list(self):
        # this could be read from a database
        return self.item_groups

    def apply_food_ordered(self, event):
        items = []
        for item in event.items:
            items.append(dto.ChefListItemDTO(item.id, item.description))

        self.item_groups.append(dto.ChefListGroupDTO(event.id, items=items))

    def apply_food_served(self, event):
        item = next(group for group in self.item_groups if group.id == event.id)
        item.items = filter(lambda i: i not in event.item_ids)
        if not item.items:
            self.item_group.remove(item)


class OpenTabReadModel(read_model.ReadModel):

    def __init__(self):
        self.todo_dict = {}

    def todo_list_for_waiter(self, waiter_name):
        result = []
        for table_todo in self.todo_dict.values():
            if table_todo.waiter == waiter_name:
                result.append(table_todo)

        return result

    def tab_for_table(self, tab_id):
        return self.todo_dict[tab_id]

    def active_table_numbers(self):
        return [tab.table_number for id, tab in self.todo_dict.items()]

    def apply_tab_opened(self, event):
        self.todo_dict[event.id] = dto.TabDTO(
            table_number=event.table_number,
            waiter=event.waiter,
            items_to_serve=[],
            served_items=[]
        )

    def apply_drinks_ordered(self, event):
        self.todo_dict[event.id].items_to_serve += event.items

    def apply_food_ordered(self, event):
        self.todo_dict[event.id].items_to_serve += event.items

    def apply_drinks_served(self, event):
        self.todo_dict[event.id].items_to_serve = \
            filter(lambda x: x.id not in event.item_ids)
        self.todo_dict[event.id].served_items = \
            filter(lambda x: x.id in event.item_ids)

    def apply_food_served(self, event):
        self.todo_dict[event.id].items_to_serve = \
            filter(lambda x: x.id not in event.item_ids)
        self.todo_dict[event.id].served_items = \
            filter(lambda x: x.id in event.item_ids)

    def apply_tab_closed(self, event):
        del self.todo_dict[event.id]
