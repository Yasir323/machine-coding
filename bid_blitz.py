"""
Problem Statement

We are developing a rewards bidding system - BidBlitz for Flipkart, where Flipkart plus members will have the opportunity to win a lavish item each day.
As an engineer, your task is to build a feature that allows members to place bids using their Flipkart Super Coins.
● The winner of the item will be the member who places the lowest bid.
● At the end of each day, the system should declare the winner.
● Members should be able to view the winners of past events.

This system aims to enhance member engagement and provide an exciting and rewarding experience for Flipkart plus users.

Explanations

What is the bid ?
a. Pledge Super coin to buy the lavish item
What is the BidBlitz Event ?
a. It is event in which members submit the bids and at the end of the event , winner is decided based on some criteria
(mentioned in the requirements)
Requirements
System should be able to add members and each member will have super coins assigned by system
a. Number of super coins assigned by system should be greater than zero
System should be able to add event where event name should be unique for each event
a. System can only add one event in a single day
Members can register for the event and only registered members can participate in the event.
Members should be able to submit bids for a particular event as per the below conditions
a. Member can only submit all bids at single go and at max 5 bids can be submitted
b. Member should have atleast max of 5 bids super coins in his wallet
i. Suppose member submit bids -> 100,500,400,800,900 ii. Then member should have at least 900 super coins
available
iii. Only the max bid would be deducted from the member wallet
In above given example, only 900 super coins will be deducted from member wallet
c. Each bid should be unique for the member for that event i. Suppose member submit 4 bids -> 100, 200, 300, 400 ii. As each bid has unique value
d. Each bid should be greater than zero
5. System admin will declare the winner.
a. How is the winner decided?
i. Member with lowest bid will be declared as winner
ii. If the lowest bid is not unique then member who submitted lowest bid first will be declared as winner
Bonus Requirement
Members can see the winners of past events.
a. How many past events can be made visible -> 5
b. Order by ascending or descending
c. Winners should be sorted by event date
Commands
ADD_MEMBER <number_of_super_coins>
a. Example : ADD_MEMBER 1 akshay 10000
b. Output : Akshay added successfully
c. Example : ADD_MEMBER 2 chris 5000
d. Output : Chris added successfully
ADD_EVENT <event_name> <prize_name>
a. Example : ADD_EVENT 1 BBD IPHONE-14 2023-06-06
b. Output : BBD with prize IPHONE-14 added successfully
REGISTER_MEMBER <member_id> <event_id>
a. Example : REGISTER_MEMBER 1 1
b. Output : Akshay registered to the BBD event successfully
SUBMIT_BID <member_id> <event_id> <bid_1> <bid_2> <bid_3> <bid_4> <bid_5> a. Example : SUBMIT_BID 1 1 100 200 400 500 600
b. Output : BIDS submitted successfully
c. Example SUBMIT_BID 2 1 100 200 400 500
d. Output : BIDS submitted successfully
e. Example : SUBMIT_BID 10 1 100 200 300 400 500
f. Output : Member did not registered for this event
DECLARE_WINNER EVENT_ID
a. Example : DECLARE_WINNER 1
b. Output : Akshay wins the IPHONE-14 with lowest bid 100
BONUS
LIST_WINNERS <order_by>
a. Example : LIST_WINNERS asc
b. Output : [ {event_id, winner_name, lowest_bid, date} ]
Guidelines

● Input can be read from a file or STDIN or coded in a driver method. [No Api and No UI]
● Output can be written to a file or STDOUT. [No Api]
● Store all interim/output data in-memory data structures. The usage of databases is not allowed.
● Restrict internet usage to looking up syntax.
● Language should be Java only.
● Save your code/project by your name and email it or upload on the google drive link provided. Your program will be executed on another machine. So, explicitly specify dependencies, if any, in your email.

Expectations

● The code should be demo-able (very important). The code should be functionally correct and complete.
● At the end of this interview round, an interviewer will provide multiple inputs to your program for which it is expected to work
● The code should handle edge cases properly and fail gracefully. Add suitable exception handling, wherever applicable.
● An example would be to display an error message when the member trying to register for same event again or member does not have enough super coins to bid
● The code should be readable, modular, testable, and extensible. Use intuitive names for your variables, methods, and classes.
● It should be easy to add/remove functionality without rewriting a lot of code.
● Do not write a monolithic code.
● Don’t use any databases.
"""

import datetime
import heapq
import time
from enum import Enum
from typing import List, Dict, Union


class Order(Enum):
    Ascending = 0
    Descending = 1


class Event:
    _id_generator = None

    @classmethod
    def get_id(cls):
        if cls._id_generator is None:
            cls._id_generator = cls._id_generator_func()
        return next(cls._id_generator)

    @classmethod
    def _id_generator_func(cls):
        i = 0
        while True:
            yield i
            i += 1

    def __init__(self, name: str, prize: str, date: str):
        self.id = Event.get_id()
        self.name = name
        self.prize = prize
        self.date = datetime.datetime.fromisoformat(date)
        self.winners = []
        self.participants = set()
        self.bids = []

    def __str__(self):
        return f"{self.id}: {self.name}"


class Member:
    _id_generator = None

    @classmethod
    def get_id(cls):
        if cls._id_generator is None:
            cls._id_generator = cls._id_generator_func()
        return next(cls._id_generator)

    @classmethod
    def _id_generator_func(cls):
        i = 0
        while True:
            yield i
            i += 1

    def __init__(self, name: str, coins: int):
        self.id = Member.get_id()
        self.name = name
        self.coins = coins
        self.events = set()

    def register(self, event_id: int):
        system = System()
        if event_id not in self.events:
            system.register_member(self.id, event_id)
            self.events.add(event_id)
            return True
        return False

    def submit_bid(self, event_id: int, bids: List[int]):
        if self.coins >= max(bids):
            if event_id in self.events:
                system = System()
                system.place_bid(self.id, event_id, bids)
                print(f"Bids placed successfully")
                self.coins -= max(bids)
        else:
            print("Insufficient coins to place the bid")


class System:

    _instance = None
    members: Dict[int, Member] = {}
    events: Dict[int, Event] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def get_event(self, event_id: int) -> Union[Event, None]:
        return self.events.get(event_id)

    def get_member(self, member_id: int) -> Union[Member, None]:
        return self.members.get(member_id)

    def add_members(self, member: Member):
        self.members[member.id] = member
        print(f"{member.name} added successfully")

    def add_event(self, event: Event):
        self.events[event.id] = event
        print(f"{event.name} added successfully")

    def register_member(self, member_id: int, event_id: int):
        if member_id in self.members and event_id in self.events:
            self.events[event_id].participants.add(member_id)

    def place_bid(self, member_id: int, event_id: int, bids: List[int]) -> bool:
        if member_id in self.members:
            if event_id in self.events:
                for bid in bids:
                    self.events[event_id].bids.append((bid, time.time_ns(), member_id))
                return True
        return False

    def declare_winner(self, event_id: int) -> str:
        bids = self.events[event_id].bids.copy()
        heapq.heapify(bids)
        winning_bid = heapq.heappop(bids)
        winner = self.get_member(winning_bid[2])
        self.events[event_id].winners.append(winner)
        return winner.name

    def list_winners(self, event_id: int, order: Order = Order.Ascending) -> List[str]:
        all_winners = self.events[event_id].winners
        if order == order.Descending:
            all_winners.sort(reverse=True)
        else:
            all_winners.sort()
        return [winner.name for winner in all_winners[:5]]


if __name__ == "__main__":
    # Create a system instance
    system = System()

    # Create members
    member1 = Member("John", 1000)
    member2 = Member("Alice", 1500)

    # Add members to the system
    system.add_members(member1)
    system.add_members(member2)

    # Create events
    event1 = Event("Event 1", "Laptop", "2024-05-10T00:00:00")
    event2 = Event("Event 2", "Smartphone", "2024-05-11T00:00:00")

    # Add events to the system
    system.add_event(event1)
    system.add_event(event2)

    # Register members for events
    member1.register(event1.id)
    member2.register(event1.id)

    # Submit bids
    member1.submit_bid(event1.id, [500, 600, 700, 800, 900])
    member2.submit_bid(event1.id, [400, 550, 750, 850, 950])

    # Declare winners
    winner = system.declare_winner(event1.id)
    print("Winner of Event 1:", winner)  # Output: Alice

    # List winners
    winners = system.list_winners(event1.id, Order.Ascending)
    print("Winners of Event 1 (Ascending):", winners)  # Output: ['Alice', 'John']

    winners_desc = system.list_winners(event1.id, Order.Descending)
    print("Winners of Event 1 (Descending):", winners_desc)  # Output: ['John', 'Alice']
