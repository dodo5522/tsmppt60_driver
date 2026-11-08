---
type: Reference
title: TriStar MPPT Daily Logger
description: Current-day measurements, events, and timing
tags: [tristar, modbus, logger]
---

# Daily logger

PDF pages 4 and 15–17 describe today's RAM values. All addresses are PDU
addresses; logical address = PDU + 1 for this table. Vscaling and Iscaling are
as defined in [scaling](scaling.md); `n` is the register value. A checked
Signed cell is explicitly signed; a blank is not explicitly defined as unsigned.

| PDU | Logical | Variable | Unit and scale | Signed cell |
|---|---:|---|---|---|
| `0x0040` | 65 | Daily minimum battery voltage | V, n × Vscaling / 2^15 | checked |
| `0x0041` | 66 | Daily maximum battery voltage | V, n × Vscaling / 2^15 | checked |
| `0x0042` | 67 | Daily maximum input voltage | V, n × Vscaling / 2^15 | checked |
| `0x0043` | 68 | Daily charge | Ah, n × 0.1 | blank |
| `0x0044` | 69 | Daily charge | Wh; see discrepancy below | blank |
| `0x0045` | 70 | Daily event flags | bitfield | blank |
| `0x0046` | 71 | Daily maximum output power | W, n × Vscaling × Iscaling / 2^17 | blank |
| `0x0047` | 72 | Daily minimum battery temperature | °C, -127 to 127 | checked |
| `0x0048` | 73 | Daily maximum battery temperature | °C, -127 to 127 | checked |
| `0x0049` | 74 | Daily faults | bitfield | blank |
| `0x004A` | 75 | Reserved | — | — |
| `0x004B`/`0x004C` | 76/77 | Daily alarms HI/LO | bitfield | blank |
| `0x004D` | 78 | Daily absorption time | seconds | blank |
| `0x004E` | 79 | Daily equalization time | seconds | blank |
| `0x004F` | 80 | Daily float time | seconds | blank |

Event flags are sticky: bit 0 reset detected, 1 equalization triggered, 2 entered
float, 3 an alarm occurred, and 4 a fault occurred. Daily fault and alarm bits
are sticky and use the same bit positions as the current
[faults and alarms](faults-alarms.md). The three stage timers are cumulative
and reset at night.

The descriptions say the daily readings are stored at the end of the charging
day. Several say a new record is created “X hours” after NIGHT without defining X;
the Wh description instead says dawn the next day. The source table does not
specify a scaling factor for Wh and the revision history says its scaling changed
from 0.1 to 1, while the description says it reports increments of 10 Wh. Do
not conflate resolution and scaling without verification. The `0x0042` heading
says array voltage, while its prose says battery voltage. On page 16 the prose
labels for maximum power and temperatures mistakenly say bitfield; the page 4
table gives W and °C respectively.
