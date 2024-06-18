"""

Functional Requirements:

Park a vehicle.
Unpark a vehicle.
Check available parking slots.
Display parking lot status.
Support different types of vehicles (e.g., car, bike, truck).
-------------------------------------------------------------

Non-functional Requirements:

The system should be scalable.
The system should be highly available.
Quick retrieval and parking operations.
-------------------------------------------------------------

Components

Parking Lot: Represents the entire parking lot.
Parking Slot: Represents an individual parking space.
Vehicle: Represents the vehicles (e.g., car, bike, truck).
Ticket: Represents a parking ticket issued when a vehicle is parked.
Parking Display Board: Displays the status of the parking lot.
Entrance/Exit Gates: Handles the entry and exit of vehicles.
-------------------------------------------------------------

Class Diagram

+------------------+
|    ParkingLot    |
+------------------+
| - levels         |
| - totalSlots     |
+------------------+
| + parkVehicle()  |
| + unparkVehicle()|
| + getStatus()    |
+------------------+

+------------------+
|    ParkingSlot   |
+------------------+
| - slotNumber     |
| - isOccupied     |
| - vehicle        |
| - type           |
+------------------+
| + park()         |
| + unpark()       |
| + isAvailable()  |
+------------------+

+------------------+
|     Vehicle      |
+------------------+
| - licensePlate   |
| - type           |
+------------------+
| + getType()      |
+------------------+

+------------------+
|     Ticket       |
+------------------+
| - ticketNumber   |
| - vehicle        |
| - entryTime      |
| - exitTime       |
+------------------+
| + generateTicket()|
| + closeTicket()  |
+------------------+

+------------------+
| ParkingDisplayBoard|
+------------------+
| - availableSlots |
+------------------+
| + displayStatus()|
+------------------+

+------------------+
|   EntranceGate   |
+------------------+
| - gateNumber     |
| - isOpen         |
+------------------+
| + openGate()     |
| + closeGate()    |
+------------------+

+------------------+
|    ExitGate      |
+------------------+
| - gateNumber     |
| - isOpen         |
+------------------+
| + openGate()     |
| + closeGate()    |
+------------------+

"""
import random
from typing import List, Optional
import datetime
from enum import Enum


class VehicleType(Enum):
    TwoWheeler = "2-Wheeler"
    ThreeWheeler = "3-Wheeler"
    FourWheeler = "4-Wheeler"


class Vehicle:

    def __init__(self, vehicle_number: str, vehicle_type: VehicleType):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type

    def __str__(self) -> str:
        return f"Vehicle: {self.vehicle_number} - {self.vehicle_type}"


class Ticket:
    ticket_counter = 0

    def __init__(self, vehicle: Vehicle, slot_number: int):
        Ticket.ticket_counter += 1
        self.ticket_number = Ticket.ticket_counter
        self.vehicle = vehicle
        self.slot_number = slot_number
        self.entry_time = datetime.datetime.now()
        self.exit_time = None
        self.fare = 0.0
        self.is_paid = False

    def close_ticket(self) -> None:
        self.exit_time = datetime.datetime.now()
        payment = Payment()
        self.is_paid, self.fare = payment.make_payment(self)

    def get_payment_status(self):
        return self.is_paid


class Payment:

    def __init__(self, hourly_rate: float = 20.0):
        self.hourly_rate = hourly_rate

    def calculate_fare(self, ticket: Ticket):
        duration = ticket.exit_time - ticket.entry_time
        hours_parked = duration.total_seconds() // 3600 + 1
        fare = self.hourly_rate * hours_parked
        print(f"Total fare: {fare:.2f}")
        return fare

    def make_payment(self, ticket: Ticket):
        fare = self.calculate_fare(ticket)
        self.pay()
        return True, fare

    def pay(self):
        pass


class ParkingSlot:
    parking_counter = 0

    def __init__(self, type_: VehicleType):
        ParkingSlot.parking_counter += 1
        self.slot_number = ParkingSlot.parking_counter
        self.type = type_
        self.is_occupied = False
        self.vehicle = None

    def park(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_occupied = True

    def un_park(self):
        self.vehicle = None
        self.is_occupied = False

    def is_available(self):
        return not self.is_occupied

    def get_slot_number(self):
        return self.slot_number

    def __str__(self) -> str:
        return f"Parking Slot: {self.slot_number} - IsAvailable: {self.is_available()}"


class Gate:
    def __init__(self, gate_number: int):
        self.gate_number = gate_number
        self.is_open = False

    def open_gate(self):
        raise NotImplemented

    def close_gate(self):
        raise NotImplemented


class EntryGate(Gate):

    def __init__(self, gate_number: int):
        super().__init__(gate_number)

    def open_gate(self):
        self.is_open = True
        print(f"Entry gate {self.gate_number} opened!")

    def close_gate(self):
        self.is_open = False
        print(f"Entry gate {self.gate_number} closed!")


class ExitGate(Gate):
    def __init__(self, gate_number: int):
        super().__init__(gate_number)

    def open_gate(self):
        self.is_open = True
        print(f"Exit gate {self.gate_number} opened!")

    def close_gate(self):
        self.is_open = False
        print(f"Exit gate {self.gate_number} closed!")


class ParkingLot:

    def __init__(self, levels: int):
        self.levels = levels
        self.parking_slots = [[]]
        self.total_slots = sum(len(slots) for slots in self.parking_slots)
        self.entry_gates = []
        self.exit_gates = []

    def add_level(self):
        self.parking_slots.append([])
        self.levels += 1

    def add_parking_slot(self, level: int, slot: ParkingSlot):
        try:
            self.parking_slots[level].append(slot)
            self.total_slots += 1
        except:
            raise Exception("Invalid level or slot")

    def add_entry_gate(self):
        pass

    def add_exit_gate(self):
        pass

    def park_vehicle(self, vehicle: Vehicle):
        for level in self.parking_slots:
            for slot in level:
                if slot.is_available():
                    slot.park(vehicle)
                    return Ticket(vehicle, slot.get_slot_number())
        print("Parking lot is full")
        return None

    def unpark_vehicle(self, ticket: Ticket):
        for level in self.parking_slots:
            for slot in level:
                if slot.slot_number == ticket.slot_number:
                    slot.unpark()
                    exit_gate = self.exit_gates[random.randint(0, len(self.exit_gates) - 1)]
                    ticket.close_ticket()
                    if ticket.get_payment_status():
                        exit_gate.open()
                        return
                    else:
                        raise Exception("Complete Payment First")

    def get_status(self) -> None:
        for i, level in enumerate(self.parking_slots):
            print(f"Level {i + 1}:")
            for slot in level:
                print(f" Slot {slot.slot_number}: {'Occupied' if slot.is_occupied else 'Available'}")


class ParkingDisplayBoard:

    def __init__(self, parking_lot: ParkingLot):
        self.parking_lot = parking_lot

    def display_status(self):
        self.parking_lot.get_status()


def main():
    # Create a parking lot with 3 levels, each with 5 slots
    parking_lot = ParkingLot(3, 5)

    # Create a display board for the parking lot
    display_board = ParkingDisplayBoard(parking_lot)

    # Create an entrance gate and an exit gate
    entrance_gate = EntryGate(1)
    exit_gate = ExitGate(1)

    # Display the initial status of the parking lot
    display_board.display_status()

    # Open the entrance gate and park a vehicle
    vehicle1 = Vehicle("ABC123", "Car")
    entrance_gate.open_gate()
    ticket1 = parking_lot.park_vehicle(vehicle1)
    entrance_gate.close_gate()

    # Display the status of the parking lot after parking a vehicle
    display_board.display_status()

    # Open the exit gate and unpark the vehicle
    exit_gate.open_gate()
    parking_lot.unpark_vehicle(ticket1)
    exit_gate.close_gate()

    # Display the status of the parking lot after unparking the vehicle
    display_board.display_status()

    # TODO: Handle entry and exit gates


if __name__ == "__main__":
    main()
