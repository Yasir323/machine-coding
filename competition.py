"""

You're organizing a multi-event competition where participants can compete in various activities.
Each participant may participate in any number of events, and their performance is scored accordingly.
Your task is to design a system in Python using object-oriented programming principles to manage
participants and their scores across different events. Additionally, you need to implement a method to
retrieve the top three participants and their scores for each event.

"""
import random
import time


class Participant:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class Event:

    def __init__(self, name: str):
        self.name = name
        self.participants = set()
        self.scores = {}

    def add_participant(self, participant: Participant):
        self.participants.add(participant)

    def simulate(self):
        time.sleep(1)
        self.scores = {participant.name: random.randint(1, 10) for participant in self.participants}


class Competition:

    def __init__(self):
        self.events = set()

    def add_event(self, event: Event):
        self.events.add(event)

    def add_participant(self, event: Event, participant: Participant):
        if event in self.events:
            event.add_participant(participant)

    def top_three_participants(self):
        for event in self.events:
            event.simulate()
            top_three = list(sorted(event.scores.items(), reverse=True, key=lambda x: x[1]))[:3]
            print(top_three)


def main():
    comp = Competition()
    event1 = Event("Cricket")
    event2 = Event("Football")
    event3 = Event("Tennis")
    p1 = Participant("John", 20)
    p2 = Participant("Jane", 20)
    p3 = Participant("Jade", 20)
    p4 = Participant("Jim", 20)
    p5 = Participant("Jack", 20)
    p6 = Participant("Jake", 20)
    p7 = Participant("Justin", 20)
    comp.add_event(event1)
    comp.add_event(event2)
    comp.add_event(event3)
    comp.add_participant(event1, p1)
    comp.add_participant(event1, p2)
    comp.add_participant(event1, p3)
    comp.add_participant(event1, p4)
    comp.add_participant(event2, p3)
    comp.add_participant(event2, p4)
    comp.add_participant(event2, p5)
    comp.add_participant(event2, p6)
    comp.add_participant(event3, p7)
    comp.add_participant(event3, p5)
    comp.add_participant(event3, p1)
    comp.top_three_participants()


if __name__ == "__main__":
    main()
