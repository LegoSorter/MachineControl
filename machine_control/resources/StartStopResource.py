import falcon
import logging

from machine_control.motors.CameraTapeMotorsController import CameraTapeMotorsController


class StartResource:

    def __init__(self, motors_controller):
        self.motors_controller: CameraTapeMotorsController = motors_controller

    def on_get(self, req, resp):
        logging.info("[StartResource] Got request, starting the machine.")
        self.motors_controller.run()
        resp.status = falcon.HTTP_OK


class StopResource:

    def __init__(self, motors_controller):
        self.motors_controller: CameraTapeMotorsController = motors_controller

    def on_get(self, req, resp):
        logging.info("[StopResource] Got request, stopping the machine.")
        self.motors_controller.stop()
        resp.status = falcon.HTTP_OK
