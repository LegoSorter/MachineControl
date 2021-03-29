# MachineControl

## Quick start
```commandline
gunicorn3 -b 0.0.0.0:8000 --timeout 0 --reload machine_control.app
```
To start a machine:
```commandline
curl 0.0.0.0:8000/start
```
To stop a machine:
```commandline
curl 0.0.0.0:8000/stop
```
