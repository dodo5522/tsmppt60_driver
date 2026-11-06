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

The package installs both the Python API and the `tsmppt60cli` command.
To install the CLI from a local checkout, run this command from the repository
root:

```bash
python -m pip install .
```

## Usage

### Command-line interface

Read all controller groups by specifying the controller's host name or IP
address:

```bash
tsmppt60cli --host 192.168.1.20
```

By default, the command writes the status as JSON to standard output, using
the same structure as the Python API result shown below. To save it to a file:

```bash
tsmppt60cli --host 192.168.1.20 > status.json
```

Available options:

| Option | Description | Default |
| --- | --- | --- |
| `--host HOST` | Controller host name or IP address | `localhost` |
| `--port PORT` | Controller port number | `80` |
| `--debug` | Enable debug mode and include logging metadata in the output | Disabled |
| `-h`, `--help` | Show help and exit | |

For example, specify a different port and enable debug mode:

```bash
tsmppt60cli --host 192.168.1.20 --port 8080 --debug
```

With `--debug`, the output includes a timestamp, logger name, and log level
before the JSON payload, so it is no longer plain JSON.

### Python API

`TsMppt60` reads all controller groups by default. The result is a
dictionary keyed by group, with each group's status keyed by label.

```python
from tsmppt60_driver import TsMppt60

status = TsMppt60("192.168.1.20")
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
        "Battery Temperature": {"value": 25, "unit": "C"},
    },
    "SolarArray": {
        "Array Voltage": {"value": 53.41, "unit": "V"},
        "Array Current": {"value": 1.4, "unit": "A"},
        "Sweep Vmp": {"value": 53.41, "unit": "V"},
        "Sweep Voc": {"value": 60.05, "unit": "V"},
        "Sweep Pmax": {"value": 73.0, "unit": "W"},
    },
    "ChargeController": {
        "LED State": {"value": 11, "unit": "Numbers"},
        "Charge State": {"value": 3, "unit": "Numbers"},
        "Heat Sink Temperature": {"value": 30, "unit": "C"},
        "Amp Hours": {"value": 18097.9, "unit": "Ah"},
        "Kilowatt Hours": {"value": 237, "unit": "kWh"},
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
