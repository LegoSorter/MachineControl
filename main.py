from fastapi import FastAPI, status
from fastapi.responses import Response

from machine_control.motors.CameraConveyorController import CameraConveyorController

app = FastAPI()
conveyor_controller = CameraConveyorController()


@app.get("/start", status_code=status.HTTP_204_NO_CONTENT)
async def start(frequency: int = 200, duty_cycle: int = 50):
    conveyor_controller.run(hz=frequency, duty_cycle=duty_cycle)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stop", status_code=status.HTTP_204_NO_CONTENT)
async def stop():
    conveyor_controller.stop()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
