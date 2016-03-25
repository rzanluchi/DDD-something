import pytest

from base.test import TestDriver
from tab.domain.aggregates import TabAggregate
from tab.domain.commands import (OpenTab, PlaceOrder, MarkDrinksServed,
                                 CloseTab, MarkFoodServed)
from tab.domain.events import (TabOpened, DrinksOrdered, FoodOrdered,
                               DrinksServed, TabClosed, FoodServed)
from tab.exceptions import (TabNotOpen, DrinksNotOutstanding,
                            FoodNotOutstanding, MustPayEnough,
                            DrinksUnserved, FoodUnserved)


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


class TestDrinksServed(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.drink_1 = type("Drink", (), {'is_drink': True, 'id': 26,
                                          'price': 2})
        self.drink_2 = type("Drink", (), {'is_drink': True, 'id': 27,
                                          'price': 3})

    def test_mark_drink_served(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.item_ids == expected_event.item_ids
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1, self.drink_2]
        )])
        self.test_driver.when(MarkDrinksServed(
            id=123, item_ids=[26, 27]
        ))
        self.test_driver.then([DrinksServed(
            id=123, item_ids=[26, 27]
        )])

    def test_serve_unordered_drinks_should_throw_exception(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
        with pytest.raises(DrinksNotOutstanding):
            self.test_driver.when(MarkDrinksServed(
                id=123, item_ids=[26, 27]
            ))

    def test_serve_drinks_already_served_should_throw_exception(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1, self.drink_2]
        ), DrinksServed(
            id=123, item_ids=[26, 27]
        )])
        with pytest.raises(DrinksNotOutstanding):
            self.test_driver.when(MarkDrinksServed(
                id=123, item_ids=[26, 27]
            ))


class TestFoodServed(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.food_1 = type("Food", (), {'is_drink': False, 'id': 26,
                                        'price': 4})
        self.food_2 = type("Food", (), {'is_drink': False, 'id': 27,
                                        'price': 5})

    def test_mark_food_served(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.item_ids == expected_event.item_ids
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), FoodOrdered(
            id=123, items=[self.food_1, self.food_2]
        )])
        self.test_driver.when(MarkFoodServed(
            id=123, item_ids=[self.food_1.id, self.food_2.id]
        ))
        self.test_driver.then([FoodServed(
            id=123, item_ids=[self.food_1.id, self.food_2.id]
        )])

    def test_serve_unordered_food_should_throw_exception(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        )])
        with pytest.raises(FoodNotOutstanding):
            self.test_driver.when(MarkFoodServed(
                id=123, item_ids=[26, 27]
            ))

    def test_serve_drinks_already_served_should_throw_exception(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), FoodOrdered(
            id=123, items=[self.food_1, self.food_2]
        ), FoodServed(
            id=123, item_ids=[26, 27]
        )])
        with pytest.raises(FoodNotOutstanding):
            self.test_driver.when(MarkFoodServed(
                id=123, item_ids=[26, 27]
            ))


class TestCloseTab(object):

    def setup_method(self, method):
        self.test_driver = TestDriver(TabAggregate())
        self.drink_1 = type("Drink", (), {'is_drink': True, 'id': 26,
                            "price": 10})
        self.food_1 = type("Food", (), {'is_drink': False, 'id': 26,
                           "price": 10})

    def test_close_tab(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.tip_value == expected_event.tip_value,
                happened_event.order_value == expected_event.order_value,
                happened_event.amount_paid == expected_event.amount_paid
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1]
        ), DrinksServed(
            id=123, item_ids=[26]
        )])
        self.test_driver.when(CloseTab(
            id=123, amount_paid=self.drink_1.price
        ))
        self.test_driver.then([TabClosed(
            id=123, amount_paid=10, order_value=10, tip_value=0
        )])

    def test_close_tab_with_tip(self):
        def compare(happened_event, expected_event):
            return all([
                happened_event.id == expected_event.id,
                happened_event.tip_value == expected_event.tip_value,
                happened_event.order_value == expected_event.order_value,
                happened_event.amount_paid == expected_event.amount_paid
            ])
        self.test_driver.compare = compare
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1]
        ), DrinksServed(
            id=123, item_ids=[26]
        )])
        self.test_driver.when(CloseTab(
            id=123, amount_paid=self.drink_1.price + 2
        ))
        self.test_driver.then([TabClosed(
            id=123, amount_paid=12, order_value=10, tip_value=2
        )])

    def test_must_pay_enough_to_close_tab(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1]
        ), DrinksServed(
            id=123, item_ids=[26]
        )])
        with pytest.raises(MustPayEnough):
            self.test_driver.when(CloseTab(
                id=123, amount_paid=self.drink_1.price - 2
            ))

    def test_cant_close_twice(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1]
        ), DrinksServed(
            id=123, item_ids=[26]
        ), TabClosed(
            id=123, amount_paid=12, order_value=10, tip_value=2
        )])
        with pytest.raises(TabNotOpen):
            self.test_driver.when(CloseTab(
                id=123, amount_paid=self.drink_1.price + 2
            ))

    def test_cant_close_with_unserved_drinks(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), DrinksOrdered(
            id=123, items=[self.drink_1]
        )])
        with pytest.raises(DrinksUnserved):
            self.test_driver.when(CloseTab(
                id=123, amount_paid=self.drink_1.price + 2
            ))

    def test_cant_close_with_unserved_food(self):
        self.test_driver.given([TabOpened(
            id=123, table_number=42, waiter="John Doe"
        ), FoodOrdered(
            id=123, items=[self.food_1]
        )])
        with pytest.raises(FoodUnserved):
            self.test_driver.when(CloseTab(
                id=123, amount_paid=self.drink_1.price + 2
            ))
