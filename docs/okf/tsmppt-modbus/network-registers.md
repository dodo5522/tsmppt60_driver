---
type: Reference
title: Active Network Registers
description: Active Ethernet settings and identification
tags: [tristar, modbus, network]
---

# Active network registers

The PDF pages 4–5 give the following active RAM settings. These are PDU
addresses; the source table leaves their logical-address cells blank. Two bytes
are stored per register in the byte order shown by the source, for example
`[1][0]`; do not infer display order without checking device output.

| PDU | Source variable or content |
|---|---|
| `0x1000` | Processor B firmware version |
| `0x1001`–`0x100E` | Reserved |
| `0x100F`–`0x1010` | IP address bytes `[1][0]`, `[3][2]` |
| `0x1011`–`0x1012` | Subnet mask, same byte pattern |
| `0x1013`–`0x1014` | Gateway, same byte pattern |
| `0x1015`–`0x1016` | Primary DNS, same byte pattern |
| `0x1017`–`0x1018` | Secondary DNS, same byte pattern |
| `0x1019`–`0x101C` | Reserved |
| `0x101D`–`0x1024` | Controller ID, 16-byte ASCII string, zero terminated |
| `0x1025` | Network flags: `0x4000` DHCP enabled, zero disabled |
| `0x1026`–`0x1028` | MAC bytes `[1][0]`, `[3][2]`, `[5][4]`; read-only per revision history |
| `0x1029`–`0x1030` | NetBIOS name, 16-byte ASCII string, zero terminated |

The revision history calls NetFlags `0x1517`, unlike the active table's
`0x1025`. Keep this discrepancy visible; verify on the target firmware.

Page 7 defines basic device-identification objects `0x00` VendorName (typical
Morningstar Corp.), `0x01` ProductCode (TS-MPPT-45 or TS-MPPT-60), and `0x02`
MajorMinorRevision (hardware major/minor and software revision). It does not
claim support for other identification levels.
