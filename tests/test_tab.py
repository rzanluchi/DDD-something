from base.test import TestDriver
from domain.aggregates import TabAggregate
from domain.commands import OpenTab
from domain.events import TabOpened


class TestTabAggregate(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())

    def test_open_tab_command(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.table_number == expected_event.table_number,
                happened_event.waiter == expected_event.waiter
            ])
        self.test_driver.compare = compare
        self.test_driver.given()
        self.test_driver.when(OpenTab(
            id=123, table_number=42, waiter="John Doe"
        ))
        self.test_driver.then([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
