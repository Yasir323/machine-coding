import time
from enum import Enum
from typing import Optional


class State(Enum):

    Moving = "MOVING"
    Idle = "IDLE"
    Unavailable = "UNAVAILABLE"


class Direction(Enum):

    Up = "UP"
    Down = "DOWN"


class RequestType(Enum):

    External = "EXTERNAL"
    Internal = "INTERNAL"


class Request:

    def __init__(self,
                 src: int,
                 type_: RequestType,
                 dest: Optional[int] = None,
                 direction: Optional[Direction] = None):

        self.src = src
        self.type = type_
        self.dest = dest
        self.direction = direction


class Elevator:
    def __init__(self,
                 state: State,
                 floor: int,
                 num_floors: int,
                 direction: Optional[Direction] = None):
        self.state = state
        self.direction = direction
        self.floor = floor
        self.up_requests = [False] * num_floors
        self.down_requests = [False] * num_floors

    def send_request(self, request: Request):
        if request.type == RequestType.Internal:
            self.__serve_internal_request(request)
        else:
            self.__serve_external_request(request)

    def __serve_internal_request(self, request: Request):
        if request.dest > self.floor:
            self.up_requests[request.dest] = True
        else:
            self.down_requests[request.dest] = True

    def __serve_external_request(self, request: Request):
        if request.direction == Direction.Up:
            self.up_requests[request.src] = True
        else:
            self.down_requests[request.src] = True

    def poll_for_requests(self):
        if any(self.up_requests):
            self.state = State.Moving
            self.direction = Direction.Up
        if any(self.down_requests):
            self.state = State.Moving
            self.direction = Direction.Down

    def move_up(self):
        self.floor += 1
        print(f"Floor: {self.floor}")
        if self.up_requests[self.floor]:
            print(f"Opening at {self.floor}")
        self.up_requests[self.floor] = False

    def move_down(self):
        self.floor -= 1
        print(f"Floor: {self.floor}")
        if self.down_requests[self.floor]:
            print(f"Opening at {self.floor}")
        self.down_requests[self.floor] = False

    def stop(self):
        if self.state != State.Unavailable:
            self.state = State.Idle
        else:
            self.state = State.Unavailable

    def move(self):
        if self.direction == Direction.Up:
            if any(self.up_requests):
                self.move_up()
            elif any(self.down_requests):
                self.direction = Direction.Down
            else:
                self.stop()
        else:
            if any(self.down_requests):
                self.move_down()
            elif any(self.up_requests):
                self.direction = Direction.Up
            else:
                self.stop()

    def dispatch(self):
        while True:
            time.sleep(0.1)
            if self.state == State.Idle:
                self.poll_for_requests()
            elif self.state == State.Moving:
                self.move()
            else:
                return
