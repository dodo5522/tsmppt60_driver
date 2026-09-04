---
type: Reference
title: TriStar MPPT EEPROM Settings
description: TCP settings, charge settings, Modbus ID, and fixed array-voltage settings
tags: [tristar, modbus, eeprom, settings]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# EEPROM settings

EEPROM registers include TCP settings in the `0x151B` range and charge settings in the
`0xE000` range. They can be written with `0x06`, but writes have operational impact and
set the EEPROM-changed fault.

## TCP settings

| PDU | Logical | Name | Meaning |
|---:|---:|---|---|
| `0x151B` | 5404 | HTTPPort | Web server port; default 80 |
| `0x151C` | 5405 | MBIPPort | Modbus TCP port; default 502 |
| `0x151D` | 5406 | NetRules | bit 0: Ethernet-to-EIA-485 bridging |
| `0x151E` | 5407 | SNMPTrapRecPort | SNMP port; default 162 |
| `0x151F` | 5408 | Ethernet Power Save | bit 0: Green Ethernet |
| `0x1520` | 5409 | VLAN Enable | bit 0: VLAN tagging |
| `0x1521` | 5410 | VLAN Parameters | VID, CFI, PCP |

When bridging is enabled, Ethernet Modbus requests addressed to other devices are forwarded
to EIA-485. Both reads and writes are bridged.

## Charge settings

| PDU | Logical | Name | Unit |
|---:|---:|---|---|
| `0xE000` | 57345 | Absorption voltage | V |
| `0xE001` | 57346 | Float voltage; 0 disables | V |
| `0xE002` | 57347 | Absorption time | s |
| `0xE003` | 57348 | Absorption extension time | s |
| `0xE004` | 57349 | Absorption extension threshold | V |
| `0xE005` | 57350 | Float cancel threshold | V |
| `0xE006` | 57351 | Float exit cumulative timer | s |
| `0xE007` | 57352 | Equalize voltage; 0 disables | V |
| `0xE008` | 57353 | Equalize interval | days |
| `0xE009` | 57354 | Equalize time above Vreg | s |
| `0xE00A` | 57355 | Equalize time at Veq | s |
| `0xE00B` | 57356 | Battery service interval | days |
| `0xE00D` | 57358 | Temperature compensation coefficient | V/C |
| `0xE00E` | 57359 | High voltage disconnect | V |
| `0xE00F` | 57360 | High voltage reconnect | V |
| `0xE010` | 57361 | Maximum regulation limit | V |
| `0xE011`/`0xE012` | 57362/57363 | Temperature compensation max/min | C |
| `0xE015`-`0xE018` | 57366-57369 | LED voltage thresholds | V |
| `0xE019` | 57370 | Modbus ID; 1-247 | - |
| `0xE01A` | 57371 | MeterBus ID; 1-15 | - |
| `0xE01D` | 57374 | Battery current limit; 0 uses default 60 A | A |
| `0xE020` | 57377 | Fixed array voltage initial value | V |
| `0xE021` | 57378 | Fixed array voltage percentage initial value | % |

Non-zero `0xE020`/`0xE021` values are copied at startup to RAM `0x005A`/`0x005B` and
disable MPPT sweeping and tracking. On the RAM side, non-zero fixed voltage `0x005A`
takes precedence over percentage `0x005B`. The source note on page 22 says that
`EVa_ref_fixed_init (0xE021)` overrides this setting, which conflicts with the address
mapping and may be a source typo; verify on hardware.

The source table lists `EV_tempcomp` (`0xE00D`) with Logical Address `57558`, but the
surrounding sequence indicates `57358` is intended. This source inconsistency must not be
silently normalized in an implementation.

## Read-only identity

`0xE0C0`-`0xE0C3` contain the ASCII serial number. `0xE0CC` is the model flag
(`0=TS-MPPT-45`, `1=TS-MPPT-60`). `0xE0CD` stores hardware version with major in the
upper byte and minor in the lower byte.
