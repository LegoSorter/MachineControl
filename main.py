from fastapi import FastAPI, status
from fastapi.responses import Response

from machine_control.motors.CameraConveyorController import CameraConveyorController
from machine_control.motors.SplittingConveyorController import SplittingConveyorController

app = FastAPI()
camera_conveyor_controller = CameraConveyorController()
splitting_conveyor_controller = SplittingConveyorController()


@app.get("/start", status_code=status.HTTP_204_NO_CONTENT)
async def start(frequency: int = 15, duty_cycle: int = 50):
    camera_conveyor_controller.run(hz=frequency, duty_cycle=duty_cycle)
    splitting_conveyor_controller.run()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stop", status_code=status.HTTP_204_NO_CONTENT)
async def stop():
    camera_conveyor_controller.stop()
    splitting_conveyor_controller.stop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/start_camera_conveyor", status_code=status.HTTP_204_NO_CONTENT)
async def start_camera_conveyor(frequency: int = 15, duty_cycle: int = 50):
    camera_conveyor_controller.run(hz=frequency, duty_cycle=duty_cycle)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stop_camera_conveyor", status_code=status.HTTP_204_NO_CONTENT)
async def stop_camera_conveyor():
    camera_conveyor_controller.stop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/start_splitting_conveyor", status_code=status.HTTP_204_NO_CONTENT)
async def start_splitting_conveyor(frequency: int = 20, duty_cycle: int = 40):
    splitting_conveyor_controller.run(hz=frequency, duty_cycle=duty_cycle)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stop_splitting_conveyor", status_code=status.HTTP_204_NO_CONTENT)
async def stop_splitting_conveyor():
    splitting_conveyor_controller.stop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
