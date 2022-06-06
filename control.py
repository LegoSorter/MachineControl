from threading import Thread
from typing import Optional
import RPi.GPIO as GPIO
import time
import falcon

LEFT = 1
RIGHT = 0


class Pin:
    def __init__(self, index):
        self.index = index
        GPIO.setup(index, GPIO.OUT)
        GPIO.output(index, GPIO.HIGH)

    def set_state(self, state):
        GPIO.output(self.index, state)


class Motor:
    def __init__(self, control_pin: Pin, direction_pin: Optional[Pin]):
        self.control_pin = control_pin
        self.direction_pin = direction_pin
        self.direction = RIGHT
        self.current_pos = 0
        self.target_pos = 0
        self.stop = False
        self.is_moving = False
        self.move_no_stop = False

    def step(self, interval=0.01):
        self.control_pin.set_state(GPIO.HIGH)
        time.sleep(interval)
        self.control_pin.set_state(GPIO.LOW)

    def move(self, steps: int):
        self.target_pos = steps

    def is_ready(self):
        return not self.is_moving

    def move_start(self):
        self.move_no_stop = True

    def move_stop(self):
        self.target_pos = self.current_pos
        self.move_no_stop = False

    def main_loop(self, interval=0.003, action_interval=0.00001):
        print("Motor started")
        if self.direction_pin:
            self.direction_pin.set_state(self.direction)
        # it = 0
        # vib_count = 0
        while not self.stop:
            # if it % 20 == 0:
            #     vib_count += 1
            #     if vib_count % 2 == 0:
            #         self.target_pos += 3
            #     else:
            #         self.target_pos -= 3
            if not self.move_no_stop:
                if self.target_pos < self.current_pos and self.direction == RIGHT:
                    self.direction = LEFT
                    if self.direction_pin:
                        self.direction_pin.set_state(LEFT)
                elif self.target_pos > self.current_pos and self.direction == LEFT:
                    self.direction = RIGHT
                    if self.direction_pin:
                        self.direction_pin.set_state(RIGHT)

                if self.current_pos != self.target_pos:
                    self.is_moving = True
                    self.step(action_interval)
                    self.current_pos += 1 if self.direction == RIGHT else -1

                if self.current_pos == self.target_pos:
                    self.is_moving = False
            else:
                self.step(action_interval)
            time.sleep(interval)


class WallResource:
    def __init__(self):
        print("init start")
#        control_pin = 11
#        direction_pin = 13
        control_pin = 29
        direction_pin = 31
        self.motor = Motor(Pin(control_pin), Pin(direction_pin))
        thread = Thread(target=self.motor.main_loop)
        thread.start()
        print("init end")

    def on_get(self, req, resp):
        """Handles GET requests"""
        print("on_get")
        qs = falcon.uri.parse_query_string(req.query_string)
        pos = qs["action"]
        self.motor.move(int(pos))
        resp.media = {"status": 0}
        print("on_end")


class SortResource:
    def __init__(self):
        self.busy = False
#        self.wall = Motor(Pin(11), Pin(13))
#        self.slider = Motor(Pin(15), None)
        self.wall = Motor(Pin(29), Pin(31))
        self.slider = Motor(Pin(33), None)
        thread_wall = Thread(target=self.wall.main_loop)
        thread_wall.start()
        thread_slider = Thread(target=self.slider.main_loop)
        thread_slider.start()

    def wait_for_positon_and_start(self):
        while not self.wall.is_ready():
            time.sleep(0.5)
        self.slider.move(self.slider.current_pos+1500)
        while not self.slider.is_ready():
            time.sleep(0.5)
        self.busy = False

    def on_get(self, req, resp):
        """Handles GET requests"""
        if self.busy:
            resp.media = {"status": 1}
            return
        self.busy = True
        qs = falcon.uri.parse_query_string(req.query_string)
        pos = qs["action"]
        self.wall.move(int(pos))
        thread = Thread(target=self.wait_for_positon_and_start)
        thread.start()
        resp.media = {"status": 0}


class SliderResource:
    def __init__(self):
#        control_pin = 15
        control_pin = 33
        self.motor = Motor(Pin(control_pin), None)
        thread = Thread(target=self.motor.main_loop)
        thread.start()

    def on_get(self, req, resp):
        """Handles GET requests"""
        qs = falcon.uri.parse_query_string(req.query_string)
        action = qs["action"]
        if action == "start":
            self.motor.move_start()
        if action == "stop":
            self.motor.move_stop()
        resp.media = {"status": 0}


GPIO.setmode(GPIO.BOARD)

#roller_pin = 15
roller_pin = 33

print("Start")

print("Thread started")
api = falcon.API()
api.add_route('/wall', WallResource())
api.add_route('/slider', SliderResource())
api.add_route('/sort', SortResource())
# while not finish or motor.is_moving:
#     print("------")
#     print(motor.current_pos)
#     print(motor.target_pos)
#     print(motor.direction)
#     action = input()
#     if action == "X":
#         motor.move(0)
#         time.sleep(3)
#         finish = True
#         motor.moving = True
#
#         continue
#     motor.move(int(action))
