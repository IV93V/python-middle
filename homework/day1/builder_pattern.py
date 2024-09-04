from abc import ABC, abstractmethod

class CarAssembler(ABC):
    @property
    @abstractmethod
    def product(self):
        pass

    @abstractmethod
    def chassis(self):
        pass

    @abstractmethod
    def engine(self):
        pass

    @abstractmethod
    def mech_gear(self):
        pass

    @abstractmethod
    def auto_gear(self):
        pass

    @abstractmethod
    def airbag(self):
        pass

    @abstractmethod
    def multimedia(self):
        pass

    @abstractmethod
    def seat_heater(self):
        pass

    @abstractmethod
    def parktronic(self):
        pass


class Car():
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def list_parts(self):
        print(f'Комплектация: {", ".join(self.parts)}')

class CarSedan(CarAssembler):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Car()

    @property
    def product(self) -> Car:
        product = self._product
        self.reset()
        return product

    def chassis(self):
        self._product.add("Корпус: Седан")

    def engine(self):
        self._product.add("Двигатель: 1,6л")

    def mech_gear(self):
        self._product.add("Коробка передач: механическая")

    def auto_gear(self):
        self._product.add("Коробка передач: автоматическая")

    def airbag(self):
        self._product.add("Подушки безопасности")

    def multimedia(self):
        self._product.add("Мультимедийная система")

    def seat_heater(self):
        self._product.add("Подогрев сидений")

    def parktronic(self):
        self._product.add("Помощь при парковке")


class CarUniversal(CarAssembler):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Car()

    @property
    def product(self) -> Car:
        product = self._product
        self.reset()
        return product

    def chassis(self):
        self._product.add("Корпус: Универсал")

    def engine(self):
        self._product.add("Двигатель: 1,8л")

    def mech_gear(self):
        self._product.add("Коробка передач: механическая")

    def auto_gear(self):
        self._product.add("Коробка передач: автоматическая")

    def airbag(self):
        self._product.add("Подушки безопасности")

    def multimedia(self):
        self._product.add("Мультимедийная система")

    def seat_heater(self):
        self._product.add("Подогрев сидений")

    def parktronic(self):
        self._product.add("Помощь при парковке")


class Director:
    def __init__(self):
        self.builder = None

    @property
    def builder(self) -> Car:
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder


    def minimal(self):
        self.builder.chassis()
        self.builder.engine()
        self.builder.mech_gear()
        self.builder.airbag()

    def standart(self):
        self.builder.chassis()
        self.builder.engine()
        self.builder.auto_gear()
        self.builder.airbag()
        self.builder.multimedia()

    def luxe(self):
        self.builder.chassis()
        self.builder.engine()
        self.builder.auto_gear()
        self.builder.airbag()
        self.builder.multimedia()
        self.builder.seat_heater()
        self.builder.parktronic()

""" 
Для проверок:

from day1.builder_pattern import *

director = Director()
builder = CarSedan()
director.builder = builder
	
director.minimal()
builder.product.list_parts()
print("\n")

director.standart()
builder.product.list_parts()
print("\n")

director.luxe()
builder.product.list_parts()
print("\n")

builder = CarUniversal()
director.builder = builder

director.minimal()
builder.product.list_parts()
print("\n")

director.standart()
builder.product.list_parts()
print("\n")

director.luxe()
builder.product.list_parts()
"""