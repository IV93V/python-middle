from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, price):
        pass


class ObserveTarget(ABC):
    @abstractmethod
    def add_observer(self, target: Observer):
        pass

    @abstractmethod
    def remove_observer(self, target: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Product(ObserveTarget):
    def __init__(self, price):
        self.__price = price
        self.__observers: List[Observer] = []

    def change_price(self, price):
        self.__price = price
        self.notify()

    def add_observer(self, target: Observer):
        self.__observers.append(target)

    def remove_observer(self, target: Observer):
        self.__observers.remove(target)

    def pint_observers(self):
        print(self.__observers)

    def notify(self):
        for x in self.__observers:
            x.update(self.__price)


class Customer(Observer):
    def __init__(self, obj: ObserveTarget, condition: bool, price_to_notify: int):
        self.__product = obj
        self.__condition = condition
        self.__price_to_notify = price_to_notify
        obj.add_observer(self)


    def update(self, price):
        if (self.__condition == True):
             if price >= self.__price_to_notify:
               print(f'{self} Цена изменилась и стала выше установленной {self.__price_to_notify}. Цена сейчас - {price}')
        else:
            if price <= self.__price_to_notify:
                 print(f'{self} Цена изменилась и стала ниже установленной {self.__price_to_notify}. Цена сейчас - {price}')


    def remove_observer(self):
        self.__product.remove_observer(self)


"""
Для проверок:

from day1.observer_pattern import *

product1 = Product(1000)
product2 = Product(2000)

customer1 = Customer(product1,1,1500)
customer2 = Customer(product1,0,1200)
customer3 = Customer(product1,0,900)
customer4 = Customer(product1,0,800)
customer5 = Customer(product2,1,2400)
customer6 = Customer(product2,1,2200)
customer7 = Customer(product2,0,2100)
customer8 = Customer(product2,0,2200)

product2.change_price(2800)
product1.change_price(200)
"""