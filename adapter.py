from abc import ABC, abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TARGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TS(ABC):
    @abstractmethod
    def getTemp(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADAPTEE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TS4_Adaptee:
    @staticmethod
    def getTSTemp():
        return 32.2


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADAPTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TS_Adapter(TS):
    def __init__(self):
        self.TS4 = TS4_Adaptee()

    def getTemp(self):
        return self.TS4.getTSTemp()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TS1(TS):
    @staticmethod
    def getTemp():
        return 22.0


class TS2(TS):
    @staticmethod
    def getTemp():
        return 25.0


class TS3(TS):
    @staticmethod
    def getTemp():
        return 21.8


ts4 = TS_Adapter()
print(ts4.getTemp())

ts2 = TS2()
print(ts2.getTemp())