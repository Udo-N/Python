from abc import ABC, abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COMPONENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Beverage(ABC):
    def __init__(self):
        self.description = "Beverage"

    def getDescription(self):
        return self.description

    @abstractmethod
    def cost(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE COMPONENTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DarkRoast(Beverage):
    def __init__(self):
        self.description = "Dark Roast"

    @staticmethod
    def cost():
        return 1.99


class HouseBlend(Beverage):
    def __init__(self):
        self.description = "House Blend"

    @staticmethod
    def cost():
        return 2.99


class Decaf(Beverage):
    def __init__(self):
        self.description = "Decaf"

    @staticmethod
    def cost():
        return 3.99


class Espresso(Beverage):
    def __init__(self):
        self.description = "Espresso"

    @staticmethod
    def cost():
        return 4.99


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DECORATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CondimentDecorator(Beverage):
    @abstractmethod
    def getDescription(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE DECORATORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Mocha(CondimentDecorator):
    def __init__(self, beverage):
        self.beverage = beverage

    def getDescription(self):
        return self.beverage.getDescription() + " + Mocha"

    def cost(self):
        return 0.20 + self.beverage.cost()


class Milk(CondimentDecorator):
    def __init__(self, beverage):
        self.beverage = beverage

    def getDescription(self):
        return self.beverage.getDescription() + " + Milk"

    def cost(self):
        return 0.30 + self.beverage.cost()


class Soya(CondimentDecorator):
    def __init__(self, beverage):
        self.beverage = beverage

    def getDescription(self):
        return self.beverage.getDescription() + " + Soya"

    def cost(self):
        return 0.40 + self.beverage.cost()


class WhippedCream(CondimentDecorator):
    def __init__(self, beverage):
        self.beverage = beverage

    def getDescription(self):
        return self.beverage.getDescription() + " + Whipped Cream"

    def cost(self):
        return 0.10 + self.beverage.cost()


cofee = DarkRoast()
print(cofee.getDescription(), ("$" + str(cofee.cost())))

cofee = Mocha(cofee)
print(cofee.getDescription(), ("$" + str(cofee.cost())))

cofee = Milk(cofee)
print(cofee.getDescription(), ("$" + str(cofee.cost())))

cofee2 = Decaf()
print(cofee2.getDescription(), ("$" + str(cofee2.cost())))

cofee2 = Soya(cofee2)
print(cofee2.getDescription(), ("$" + str(cofee2.cost())))