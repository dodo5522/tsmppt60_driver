# TS-MPPT-60 driver module

Python driver module for reading status data from a TS-MPPT-60 charge
controller.

The public API exposes the following controller groups:

- `Battery`
  - Battery Voltage
  - Target Voltage
  - Charge Current
  - Output Power
  - Battery Temperature
- `SolarArray`
  - Array Voltage
  - Array Current
  - Sweep Vmp
  - Sweep Voc
  - Sweep Pmax
- `ChargeController`
  - LED State
  - Charge State
  - Heat Sink Temperature
  - Amp Hours
  - Kilowatt Hours

## Requirements

- Python 3.11 or later, before 3.15

## Installation

```bash
pip install tsmppt60-driver
```

## Usage

`SystemStatus` reads all controller groups by default. The result is a
dictionary keyed by group, with each group's status keyed by label.

```python
from tsmppt60_driver import SystemStatus

status = SystemStatus("192.168.1.20")
print(status.get())
```

The result has the following structure:

```python
{
    "Battery": {
        "Battery Voltage": {"value": 23.93, "unit": "V"},
        "Target Voltage": {"value": 28.6, "unit": "V"},
        "Charge Current": {"value": 3.2, "unit": "A"},
        "Output Power": {"value": 76.0, "unit": "W"},
        "Battery Temperature": {"value": 25.0, "unit": "C"},
    },
    "SolarArray": {
        "Array Voltage": {"value": 53.41, "unit": "V"},
        "Array Current": {"value": 1.4, "unit": "A"},
        "Sweep Vmp": {"value": 53.41, "unit": "V"},
        "Sweep Voc": {"value": 60.05, "unit": "V"},
        "Sweep Pmax": {"value": 73.0, "unit": "W"},
    },
    "ChargeController": {
        "LED State": {"value": 11, "unit": ""},
        "Charge State": {"value": 3, "unit": ""},
        "Heat Sink Temperature": {"value": 30.0, "unit": "C"},
        "Amp Hours": {"value": 18097.9, "unit": "Ah"},
        "Kilowatt Hours": {"value": 237.0, "unit": "kWh"},
    },
}
```

To read only selected groups, pass their names using the keyword-only
`groups` argument:

```python
status.get(groups={"Battery"})
```

The `groups` property returns the available group names:

```python
print(status.groups)
# {'Battery', 'SolarArray', 'ChargeController'}
```

Individual controllers are also available from the top-level package:

```python
from tsmppt60_driver import Battery

battery = Battery("192.168.1.20", 80)
print(battery.labels)
print(battery.get())
```

To serialize the result as JSON:

```python
import json

print(json.dumps(status.get()))
```
