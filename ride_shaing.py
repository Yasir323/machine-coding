from collections import namedtuple
from enum import Enum, auto, StrEnum
from typing import List, Union


def generate_id():
    i = 0
    while True:
        yield i
        i += 1


get_id = generate_id()


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class Strategy(Enum):
    MOST_VACANT: auto()
    PREFERRED_VEHICLE: auto()


Coordinates = namedtuple("Coordinates", ["latitude", "longitude"])
Ride = namedtuple("Ride", ["id", "driver", "vehicle", "origin", "destination", "available_seats"])
DriverTuple = namedtuple("Driver", ["id", "name", "age", "gender", "vehicles"])
PassengerTuple = namedtuple("Passenger", ["id", "name", "age", "gender"])


class Driver:

    def __init__(self, name: str, age: int, gender: Gender, vehicles: List[str]):
        self.driver = DriverTuple(next(get_id), name, age, gender.value, vehicles)

    def save(self):
        drivers = Drivers()
        drivers.add(self.driver)

    def offer_ride(self, vehicle: str, origin: Coordinates, destination: Coordinates,
                   available_seats: int):
        ride = Ride(next(get_id), self.driver, vehicle, origin, destination, available_seats)
        rides = Rides()
        rides.add(ride)

    def add_vehicle(self, vehicle: str):
        self.driver.vehicles.append(vehicle)
        drivers = Drivers()
        drivers.update(self.driver)


class Passenger:
    def __init__(self, name: str, age: int, gender: Gender):
        self.passenger = PassengerTuple(next(get_id), name, age, gender.value)

    def save(self):
        passengers = Passengers()
        passengers.add(self.passenger)

    def find_rides(self, source: Coordinates, destination: Coordinates,
                   seats: int, selection_strategy: Strategy):
        # Pick all rides with same source
        # If they have same destinations return them
        # If all the trips have different destinations,
        # find the ones which have source as the destinations that we have
        pass


class Drivers(Singleton):

    def __init__(self):
        self.drivers = []

    def add(self, driver: DriverTuple) -> int:
        self.drivers.append(driver)
        return driver.id

    def delete(self, driver_id: int) -> bool:
        index = -1
        for i, driver in enumerate(self.drivers):
            if driver.id == driver_id:
                index = i
                break
        if index != -1:
            self.drivers.pop(index)
            return True
        return False

    def get(self, driver_id: int) -> Union[DriverTuple, None]:
        res = list(filter(lambda x: x.id == driver_id, self.drivers))
        return res if res else None

    def update(self, d: DriverTuple) -> bool:
        for i, driver in enumerate(self.drivers):
            if driver.id == d.id:
                driver.vehicles = d.vehicles
                return True
        return False


class Passengers(Singleton):

    def __init__(self):
        self.passengers = []

    def add(self, passenger: PassengerTuple) -> int:
        self.passengers.append(passenger)
        return passenger.id

    def delete(self, passenger_id: int) -> bool:
        index = -1
        for i, passenger in enumerate(self.passengers):
            if passenger.id == passenger_id:
                index = i
                break
        if index != -1:
            self.passengers.pop(index)
            return True
        return False

    def get(self, passenger_id: int) -> Union[PassengerTuple, None]:
        res = list(filter(lambda x: x.id == passenger_id, self.passengers))
        return res if res else None


class Rides(Singleton):

    def __init__(self):
        self.rides = []

    def add(self, ride: Ride):
        self.rides.append(ride)

    def delete(self, ride_id: int) -> bool:
        target = -1
        for index, ride in enumerate(self.rides):
            if ride.id_ == ride_id:
                break
        if target != -1:
            self.rides.pop(target)
            return True
        return False

# class VehicleDb:
#
#     def __init__(self):
#         self.vehicles = []
#
#     def add(self, vehicle: Vehicle) -> int:
#         pass
#
#     def delete(self, vehicle_id: int) -> bool:
#         pass
#
#     def get(self, vehicle_id: int) -> Vehicle:
#         pass
