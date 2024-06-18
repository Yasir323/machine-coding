import threading
import time
import unittest
from elevator_syatem import Elevator, State, Direction, Request, RequestType


class TestElevator(unittest.TestCase):
    def setUp(self):
        # Initialize elevator for testing
        self.num_floors = 10
        self.elevator = Elevator(state=State.Idle, floor=0, num_floors=self.num_floors)

    def test_send_internal_request(self):
        # Test internal request handling
        internal_request = Request(src=2, type_=RequestType.Internal, dest=7)
        self.elevator.send_request(internal_request)
        self.assertTrue(self.elevator.up_requests[7])

    def test_send_external_request(self):
        # Test external request handling
        external_request = Request(src=5, type_=RequestType.External, direction=Direction.Up)
        self.elevator.send_request(external_request)
        self.assertTrue(self.elevator.up_requests[5])

    def test_move_up(self):
        # Test moving up
        self.elevator.up_requests[1] = True
        self.elevator.direction = Direction.Up
        self.elevator.move()
        self.assertEqual(self.elevator.floor, 1)

    def test_move_down(self):
        # Test moving down
        self.elevator.down_requests[3] = True
        self.elevator.move()
        self.assertEqual(self.elevator.floor, -1)

    def test_stop_when_unavailable(self):
        # Test stop when elevator is unavailable
        self.elevator.state = State.Unavailable
        self.elevator.stop()
        self.assertEqual(self.elevator.state, State.Unavailable)

    def test_full_scenario(self):
        # Test a complete scenario
        self.elevator.send_request(Request(src=2, type_=RequestType.External, direction=Direction.Up))
        self.elevator.send_request(Request(src=4, type_=RequestType.Internal, dest=8))
        t = threading.Thread(target=self.elevator.dispatch)
        t.start()
        # Stop the thread/elevator
        time.sleep(5)
        self.elevator.state = State.Unavailable
        self.assertEqual(self.elevator.floor, 8)


if __name__ == "__main__":
    unittest.main()
