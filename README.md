# MachineControl

## Quick start
```commandline
uvicorn main:app --host 0.0.0.0 --port 8000
```
To start a machine:
```commandline
curl 0.0.0.0:8000/start
```
To stop a machine:
```commandline
curl 0.0.0.0:8000/stop
```
