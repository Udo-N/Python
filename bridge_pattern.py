from abc import ABC, abstractmethod
import math


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IMPLEMENTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Color(ABC):
    @abstractmethod
    def drawShape(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE IMPLEMENTORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Red(Color):
    @staticmethod
    def drawShape(shape, area):
        print("Drawing red", shape, "with area", area, "meters")


class Blue(Color):
    @staticmethod
    def drawShape(shape, area):
        print("Drawing blue", shape, "with area", area, "meters")


class Green(Color):
    @staticmethod
    def drawShape(shape, area):
        print("Drawing green", shape, "with area", area, "meters")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ABSTRACTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Shape(ABC):
    @abstractmethod
    def Draw(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REFINED ABSTRACTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Circle(Shape):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def Draw(self):
        self.color.drawShape("circle", "{:.2f}".format(math.pi*self.radius**2))


class Rectangle(Shape):
    def __init__(self, length, breadth, color):
        self.length = length
        self.breadth = breadth
        self.color = color

    def Draw(self):
        self.color.drawShape("rectangle", "{:.2f}".format(self.length*self.breadth))


class Triangle(Shape):
    def __init__(self, base, height, color):
        self.base = base
        self.height = height
        self.color = color

    def Draw(self):
        self.color.drawShape("triangle", "{:.2f}".format(self.base*self.height))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN CODE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
blueTriangle = Triangle(20, 10, Blue())
blueTriangle.Draw()

greenCircle = Circle(5, Green())
greenCircle.Draw()

redCircle = Circle(5, Red())
redCircle.Draw()

redRectangle = Rectangle(4, 4, Red())
redRectangle.Draw()
