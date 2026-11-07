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

## Migrating from v0.2.3 to v1.0.0

Version 1.0.0 changes the public Python API and the returned data structure.
The examples below compare the `v0.2.3` tag with version 1.0.0.

### Replace SystemStatus with TsMppt60

Before (v0.2.3):

```python
from tsmppt60_driver import SystemStatus

status = SystemStatus("192.168.1.20", port=80)
data = status.get(False)
voltage = data["Battery Voltage"]["value"]
```

After (v1.0.0):

```python
from tsmppt60_driver import TsMppt60

status = TsMppt60("192.168.1.20", port=80)
data = status.get()
voltage = data["Battery"]["Battery Voltage"]["value"]
```

`SystemStatus` is no longer exported. The `is_limit` argument to `get()`
has been removed: replace both `get(False)` and `get(is_limit=False)` with
`get()`. The new default reads all available labels, including Output Power,
Battery Temperature, and the sweep values that were excluded by the old
default `get()`.

### Update data consumers and group selection

Previously, results were keyed directly by label, and each item contained
`group`, `value`, and `unit`. Results are now keyed first by group, then by
label; each item contains only `value` and `unit`. Update stored JSON
consumers and scripts to use the new nesting as well.

| v0.2.3 group | v1.0.0 group | Labels |
| --- | --- | --- |
| `Battery` | `Battery` | Battery Voltage, Target Voltage, Charge Current, Output Power |
| `Array` | `SolarArray` | Array Voltage, Array Current, Sweep Vmp, Sweep Voc, Sweep Pmax |
| `Temperature` | `Battery` | Battery Temperature |
| `Temperature` | `ChargeController` | Heat Sink Temperature |
| `Counter` | `ChargeController` | Amp Hours, Kilowatt Hours |
| `Condition` | `ChargeController` | LED State, Charge State |

Use the keyword-only `groups` argument to read selected groups:

```python
data = status.get(groups={"Battery", "SolarArray"})
```

The old `SystemStatus` iteration and `len(status)` interfaces are no longer
available. Use `status.groups` to discover group names. For direct controller
access, replace `BatteryStatus` with `Battery`, `SolarArrayStatus` with
`SolarArray`, and the temperature, counter, and operating-condition
controllers with the groups listed above. Construct these controllers with
`(host, port)` rather than a `ManagementBase` instance, and use `get()`
instead of `get_status_all()`. To select individual labels, use, for example,
`Battery("192.168.1.20", 80).get(target_labels=["Battery Voltage"])`.

### Use the installed CLI for shell scripts

The new `tsmppt60cli` command replaces the need for a Python one-liner.
For example, the old `jq` selector `'."Battery Voltage"'` becomes
`'.Battery["Battery Voltage"]'`:

```bash
tsmppt60cli --host 192.168.1.20 | jq '.Battery["Battery Voltage"]'
```

Use `tsmppt60cli` as the CLI entry point; `python -m tsmppt60_driver` is
not supported.
