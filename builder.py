from abc import ABC, abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DIRECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Engineer:
    @staticmethod
    def constructAirplane(concreteBuilder):
        concreteBuilder.buildWings()
        concreteBuilder.buildSeat()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PRODUCT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Airplane:
    def __init__(self):
        self.wingspan = None
        self.crewSeats = None

    def show(self):
        print("Wingspan:", self.wingspan)
        print("Seat Number:", self.crewSeats)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUILDER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AirplaneBuilder(ABC):
    @abstractmethod
    def buildWings(self):
        pass

    @abstractmethod
    def buildSeat(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE BUILDERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CropDuster(AirplaneBuilder):
    plane = Airplane()

    @staticmethod
    def buildWings():
        CropDuster.plane.wingspan = 9.0

    @staticmethod
    def buildSeat():
        CropDuster.plane.crewSeats = 3

    @staticmethod
    def getAirplane():
        return CropDuster.plane


class FighterJet(AirplaneBuilder):
    plane = Airplane()

    @staticmethod
    def buildWings():
        FighterJet.plane.wingspan = 35.0

    @staticmethod
    def buildSeat():
        FighterJet.plane.crewSeats = 2

    @staticmethod
    def getAirplane():
        return FighterJet.plane


class Glider(AirplaneBuilder):
    plane = Airplane()

    @staticmethod
    def buildWings():
        Glider.plane.wingspan = 57.1

    @staticmethod
    def buildSeat():
        Glider.plane.crewSeats = 1

    @staticmethod
    def getAirplane():
        return Glider.plane


myDirector = Engineer()
crop = CropDuster()
fighter = FighterJet()
glider = Glider()

myDirector.constructAirplane(crop)
built_crop_duster = crop.getAirplane()
built_crop_duster.show()

myDirector.constructAirplane(fighter)
built_fighter = fighter.getAirplane()
built_fighter.show()
