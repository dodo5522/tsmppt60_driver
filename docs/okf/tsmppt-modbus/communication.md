---
type: Reference
title: TriStar MPPT Modbus Communication
description: RTU, TCP, supported function codes, and address conventions
tags: [modbus, rtu, tcp, communication]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# Communication

## Serial

The TriStar MPPT supports Modbus RTU only.

| Parameter | Value |
|---|---|
| Baud rate | 9600 bps |
| Parity | None |
| Data bits | 8 |
| Stop bits | 1 or 2 (the controller sends 2) |
| Flow control | None |

RS-232 and EIA-485 interfaces are supported.

## TCP

TS-MPPT-60 models support Modbus TCP over Ethernet. Defaults are DHCP enabled,
TCP port 502, and Modbus ID 1. If DHCP fails, the defaults are IP `192.168.1.253`,
gateway/DNS `192.168.1.1`, and subnet mask `255.255.255.0`.

The specification notes that the TCP socket is closed after each Modbus response.

## Supported functions

- `0x01` Read Coils
- `0x02` Read Discrete Inputs
- `0x03` Read Holding Registers
- `0x04` Read Input Registers
- `0x05` Write Single Coil
- `0x06` Write Single Register
- `0x2B`, subcode `0x0E` Read Device Identification

Device Identification supports Basic Device Identification (ID code `0x01`) only.
