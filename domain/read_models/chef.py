class ChefListItemDTO(object):

    def __init__(self, item_id, description):
        self.item_id = item_id
        self.description = description


class ChefListGroupDTO(object):

    def __init__(self, tab_id, items):
        self.tab_id = tab_id
        self.items = items


class ChefReadModel(object):

    def __init__(self):
        self.item_groups = []

    def get_todo_list(self):
        # this could be read from a database
        return self.item_groups

    def event_food_ordered(self, event):
        items = []
        for item in event.items:
            items.append(ChefListItemDTO(item.id, item.description))

        self.item_groups.append(ChefListGroupDTO(event.id, items=items))

    def event_food_served(self, event):
        item = next(group for group in self.item_groups if group.id == event.id)
        item.items = filter(lambda i: i not in event.item_ids)
        if not item.items:
            self.item_group.remove(item)
