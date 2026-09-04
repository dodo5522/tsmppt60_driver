---
type: Reference
title: TriStar MPPT RAM Registers
description: Measurement, status, MPPT, daily logger, and volatile control registers
tags: [tristar, modbus, ram, registers]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# RAM Registers

RAM registers are updated continuously. The curated machine-readable definitions are in
`registers.json`.

## Core measurements

| PDU | Logical | Name | Unit |
|---:|---:|---|---|
| `0x0000`/`0x0001` | 1/2 | V_PU hi/lo | - |
| `0x0002`/`0x0003` | 3/4 | I_PU hi/lo | - |
| `0x0004` | 5 | ver_sw (BCD) | - |
| `0x0018` | 25 | Battery voltage, filtered | V |
| `0x0019` | 26 | Battery terminal voltage | V |
| `0x001A` | 27 | Battery sense voltage | V |
| `0x001B` | 28 | Array voltage | V |
| `0x001C` | 29 | Battery charge current | A |
| `0x001D` | 30 | Array current | A |
| `0x0023` | 36 | Heatsink temperature | C |
| `0x0024` | 37 | RTS temperature | C |
| `0x0025` | 38 | Battery temperature | C |

## Status and charging

| PDU | Logical | Name | Unit |
|---:|---:|---|---|
| `0x0026` | 39 | Slow battery voltage | V |
| `0x0027` | 40 | Slow charge current | A |
| `0x0028` | 41 | Minimum battery voltage | V |
| `0x0029` | 42 | Maximum battery voltage | V |
| `0x002A`/`0x002B` | 43/44 | Hourmeter HI/LO (table) | h |
| `0x002C` | 45 | Fault bitfield | - |
| `0x002E`/`0x002F` | 47/48 | Alarm HI/LO | - |
| `0x0030` | 49 | DIP switch bitfield | - |
| `0x0031` | 50 | LED state | - |
| `0x0032` | 51 | Charge state | - |
| `0x0033` | 52 | Target regulation voltage | V |
| `0x0034`/`0x0035` | 53/54 | Resettable charge Ah HI/LO | Ah |
| `0x0036`/`0x0037` | 55/56 | Total charge Ah HI/LO | Ah |
| `0x0038`/`0x0039` | 57/58 | Resettable/total charge kWh | kWh |
| `0x003A` | 59 | Last output power | W |
| `0x003B` | 60 | Last input power | W |
| `0x003C` | 61 | Last sweep maximum power | W |
| `0x003D` | 62 | Last sweep Vmp | V |
| `0x003E` | 63 | Last sweep Voc | V |

## Volatile control

- `0x0059` (logical 90) `Vb_ref_slave`: non-zero forces slave state; update within 60 seconds or a fault occurs.
- `0x005A` (logical 91) `Va_ref_fixed`: non-zero stops MPPT and fixes the array voltage.
- `0x005B` (logical 92) `Va_ref_fixed_pct`: fixes the array voltage as a percentage of Voc. Non-zero `0x005A` takes precedence.

Treat these as control inputs, not ordinary measurements.

## Source inconsistency

The register table lists the hourmeter as `0x002A=HI`, `0x002B=LO`, while the example on
page 25 uses `0x002A=LO`, `0x002B=HI`. Because the `V_PU`/`I_PU` HI/LO naming is consistent,
the table order is the more reasonable implementation interpretation. This is an inference,
not an explicit correction in the source; verify it against the target firmware or hardware.
