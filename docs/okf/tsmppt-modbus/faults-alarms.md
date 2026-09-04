---
type: Reference
title: TriStar MPPT Faults and Alarms
description: Fault and alarm bitfield definitions
tags: [tristar, modbus, faults, alarms]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# Faults and alarms

## Fault register `0x002C` / logical 45

| Bit | Fault |
|---:|---|
| 0 | Overcurrent |
| 1 | FETs shorted |
| 2 | Software bug |
| 3 | Battery HVD |
| 4 | Array HVD |
| 5 | Settings switch changed |
| 6 | Custom settings edit |
| 7 | RTS shorted |
| 8 | RTS disconnected |
| 9 | EEPROM retry limit |
| 10 | Reserved |
| 11 | Slave control timeout |
| 12 | Fault 13 |
| 13 | Fault 14 |
| 14 | Fault 15 |
| 15 | Fault 16 |

## Alarm registers `0x002E`/`0x002F`

| Bit | Alarm |
|---:|---|
| 0 | RTS open |
| 1 | RTS shorted |
| 2 | RTS disconnected |
| 3 | Heatsink sensor open |
| 4 | Heatsink sensor shorted |
| 5 | High temperature current limit |
| 6 | Current limit |
| 7 | Current offset |
| 8 | Battery sense out of range |
| 9 | Battery sense disconnected |
| 10 | Uncalibrated |
| 11 | RTS miswire |
| 12 | High voltage disconnect |
| 13 | Undefined |
| 14 | System miswire |
| 15 | MOSFET open |
| 16 | P12 voltage off |
| 17 | High input voltage current limit |
| 18 | ADC input max |
| 19 | Controller reset |
| 20-23 | Alarm 21-24 |

## Clear operations

Fault clear and alarm clear use coils `0x0014` and `0x0015`, respectively.
Daily bitfields retain events that occurred during the day.
