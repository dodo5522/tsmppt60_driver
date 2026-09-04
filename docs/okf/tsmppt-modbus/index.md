---
type: Knowledge Bundle
okf_version: "0.2"
title: TriStar MPPT Modbus
description: Implementation-oriented knowledge bundle for the TriStar MPPT-45/60 Modbus specification
tags: [tristar, ts-mppt, modbus, solar-charge-controller]
status: current
---

# TriStar MPPT Modbus

Implementation knowledge derived from Morningstar's TriStar MPPT Modbus Specification V10.2.

## Contents

- [Communication](communication.md)
- [RAM registers](ram-registers.md)
- [EEPROM settings](eeprom-settings.md)
- [Coils and commands](coils.md)
- [Scaling and word order](scaling.md)
- [Faults and alarms](faults-alarms.md)
- [Curated machine-readable register definitions](registers.json)
- [Source and maintenance](source.md)

## Implementation rules

Treat PDU addresses as the 0-based addresses listed in the specification. PDU addresses
and Logical Addresses are distinct and must not be conflated. Follow each field's stated
HI/LO order for multi-word values.

EEPROM writes, slave control, and fixed array-voltage control have operational impact.
Keep them separate from read-only operations and require an explicit write call.
