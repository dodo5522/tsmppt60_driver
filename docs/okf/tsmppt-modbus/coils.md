---
type: Reference
title: TriStar MPPT Coils and Commands
description: Coil operations and EEPROM write cautions
tags: [tristar, modbus, coils, commands]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# Coils and commands

| PDU | Logical | Operation |
|---:|---:|---|
| `0x0000` | 1 | Equalize triggered |
| `0x0002` | 3 | Charge disconnect; 1 forces disconnect state |
| `0x0010` | 17 | Resettable Ah clear (set-only) |
| `0x0011` | 18 | Total Ah clear (set-only) |
| `0x0012` | 19 | Resettable kWh clear (set-only) |
| `0x0013` | 20 | Battery service calendar reset |
| `0x0014` | 21 | Fault clear |
| `0x0015` | 22 | Alarm clear |
| `0x0016` | 23 | Force EEPROM update (set-only) |
| `0x0018` | 25 | Total kWh clear (set-only) |
| `0x0019` | 26 | Vb_min/Vb_max clear (set-only) |
| `0x00F0` | 241 | Test a single phase (test mode only) |
| `0x00FF` | 256 | Reset control |
| `0x1000`-`0x1003` | 4096-4099 | Send Test Notification 1-4 |
| `0x10FF` | 4351 | Reset communications server |

Set-only coils always read back as 0. Treat undefined coils as reserved and do not write them.

## Register writes

EEPROM writes use `0x06 Write Single Register`. The controller does not verify the written value.
Any EEPROM write sets an EEPROM-changed fault; reset the controller to clear that fault.
