# MachineControl

## Quick start
```commandline
uvicorn main:app -b 0.0.0.0:8000 --timeout 0 --reload
```
To start a machine:
```commandline
curl 0.0.0.0:8000/start
```
To stop a machine:
```commandline
curl 0.0.0.0:8000/stop
```
