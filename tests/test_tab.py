import pytest

from base.test import TestDriver
from domain.aggregates import TabAggregate
from domain.commands import OpenTab, PlaceOrder
from domain.events import TabOpened, DrinksOrdered, FoodOrdered
from domain.exceptions import TabNotOpen


class TestOpenTab(object):

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


class TestCantOrderUnopenTab(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())

    def test_cant_open_tab(self):
        self.test_driver.given()
        with pytest.raises(TabNotOpen):
            self.test_driver.when(PlaceOrder(
                id=123, items=[]
            ))


class TestPlaceDrinksOrder(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.drink_1 = type("Drink", (), {'is_drink': True})
        self.drink_2 = type("Drink", (), {'is_drink': True})

    def test_place_order(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.items == expected_event.items
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
        self.test_driver.when(PlaceOrder(
            id=123, items=[self.drink_1, self.drink_2]
        ))
        self.test_driver.then([DrinksOrdered(
            id=123, items=[self.drink_1, self.drink_2]
        )])


class TestPlaceFoodOrder(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.food_1 = type("Food", (), {'is_drink': False})
        self.food_2 = type("Food", (), {'is_drink': False})

    def test_place_order(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.items == expected_event.items
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
        self.test_driver.when(PlaceOrder(
            id=123, items=[self.food_1, self.food_2]
        ))
        self.test_driver.then([FoodOrdered(
            id=123, items=[self.food_1, self.food_2]
        )])


class TestPlaceFoodAndDrinkOrder(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.drink_1 = type("Drink", (), {'is_drink': True})
        self.food_1 = type("Food", (), {'is_drink': False})

    def test_place_order(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.items == expected_event.items
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
        self.test_driver.when(PlaceOrder(
            id=123, items=[self.food_1, self.drink_1]
        ))
        self.test_driver.then([DrinksOrdered(
            id=123, items=[self.drink_1]
        ), FoodOrdered(
            id=123, items=[self.food_1]
        )])
