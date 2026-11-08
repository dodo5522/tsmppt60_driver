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
`registers.json`. The tables below summarize names and units, not all source
columns. The original tables on PDF pages 3-4 also contain signedness and scaling;
see [Scaling and signedness](scaling.md#signedness) and the machine-readable
`source_page` and `signed_column` fields. The JSON remains a curated subset,
not a complete transcription of all RAM, EEPROM, and network registers.

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
| `0x0038` | 57 | Resettable charge kWh (one word) | kWh |
| `0x0039` | 58 | Total charge kWh (one word) | kWh |
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


## State values

PDF page 13 defines LED state `0x0031` as: 0 START, 1 START2, 2 BRANCH,
3 fast green blink, 4 slow green blink, 5 green blink at 1 Hz, 6 green,
7 undefined, 8 yellow, 9 undefined, 10 blinking red, 11 red, 12 R-Y-G error,
13 R/Y-G error, 14 R/G-Y error, 15 R-Y error (HTD), 16 R-G error (HVD),
17 R/Y-G/Y error, 18 G/Y/R error, 19 G/Y/R twice. The source does not
explain every pattern further.

Charge state `0x0032`: 0 START, 1 NIGHT_CHECK, 2 DISCONNECT, 3 NIGHT,
4 FAULT, 5 MPPT, 6 ABSORPTION, 7 FLOAT, 8 EQUALIZE, 9 SLAVE.

The slow voltage and current (`0x0026`/`0x0027`) are filtered with a time
constant of approximately one minute. Target voltage `0x0033` varies with the
charge stage and is temperature compensated. The battery temperature comes
from the ambient sensor or an attached RTS. Array current is not measured with
precision shunts and can differ from actual current by ±20% (PDF pages 9–10, 14).

## Additional filtered ADC values

PDF pages 3 and 9–10 list these signed values; `n` is the signed raw word.
The source has an apparent missing `n` in the `0x001F` formula; the formula
below preserves it rather than silently correcting it.

| PDU | Logical | Measurement | Source scaling |
|---|---:|---|---|
| `0x001E` | 31 | 12 V supply | n × 18.612 / 2^15 |
| `0x001F` | 32 | 3 V supply | 6.6 / 2^15 (no n printed) |
| `0x0020` | 33 | MeterBus supply | n × 18.612 / 2^15 |
| `0x0021` | 34 | 1.8 V supply | n × 3 / 2^15 |
| `0x0022` | 35 | External reference voltage | n × 3 / 2^15 |

`0x0024` is the optional remote temperature sensor; `0x80` indicates disconnect.
The filtered battery regulation voltage `0x0018` follows valid battery sense
voltage, otherwise terminal voltage. Battery extrema `0x0028`/`0x0029` are
long-term values reset when resettable Ah is cleared. DIP bit 0 is switch 1.

For slave control `0x0059`, writing again after timeout exits the fault and
resumes operation. Fixed-array-voltage controls `0x005A`/`0x005B` require
processor A firmware V09 or later. With percentage control, periodic Voc checks
adjust the target; changing the percentage takes effect at the next Voc check
(PDF page 17). See [daily logger](daily-logger.md) for today's RAM values and
[active network settings](network-registers.md) for network RAM values.
