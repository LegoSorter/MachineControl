import falcon

from machine_control.motors.CameraTapeMotorsController import CameraTapeMotorsController
from machine_control.resources.StartStopResource import StartResource, StopResource

api = application = falcon.API()

controller = CameraTapeMotorsController()
start_machine_resource = StartResource(controller)
stop_machine_resource = StopResource(controller)

api.add_route("/start", start_machine_resource)
api.add_route("/stop", stop_machine_resource)
