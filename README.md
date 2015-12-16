# TS-MPPT-60 driver module

This is python driver module to get the following status of TS-MPPT-60.

* Amp Hours
* Array Current
* Array Voltage
* Battery Temperature
* Battery Voltage
* Charge Current
* Heat Sink Temperature
* Kilowatt Hours
* Output Power
* Sweep Pmax
* Sweep Vmp
* Sweep Voc
* Target Voltage

# Requirement

* requests

# How to install

1. ./setup.py build
2. ./setup.py install

# How to use

SystemStatus class object is iterator containing all live status data of TS-MPPT-60. Try the following line.

```python
    print(SystemStatus("192.168.1.20").get())
```

The result is like following.

```
{'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.9},
 'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.4},
 'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
 'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 23.93},
 'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
 'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', ...},
 'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
 'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6}}
```

The above data is limited information. You can disable the limitter by setting False to the second argument as SystemStatus() class.

```python
    print(SystemStatus("192.168.1.20", False).get())
```

The result is like following.

```
{'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.8},
 'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.3},
 'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
 'Battery Temperature': {'group': 'Temperature', 'unit': 'C', ...},
 'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 24.01},
 'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
 'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', ...},
 'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
 'Output Power': {'group': 'Battery', 'unit': 'W', 'value': 76.0},
 'Sweep Pmax': {'group': 'Array', 'unit': 'W', 'value': 73.0},
 'Sweep Vmp': {'group': 'Array', 'unit': 'V', 'value': 53.41},
 'Sweep Voc': {'group': 'Array', 'unit': 'V', 'value': 60.05},
 'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6}}
```
