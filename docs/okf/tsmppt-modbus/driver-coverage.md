---
type: Reference
title: Driver Implementation Coverage
description: Mapping of current driver reads to the V10.2 specification
tags: [tristar, driver, coverage]
---

# Driver implementation coverage

This inventory describes the code at the time of issue #76. “Exposed” means the
current public controller group reads the register; it does not establish correctness
or hardware verification. PDU addresses are zero-based. Specification details are
in [RAM registers](ram-registers.md), [scaling](scaling.md), and the PDF pages
listed below. All entries are reads; the driver does not expose coil or register writes.

| PDU | Logical | Driver use | PDF pages |
|---|---|---|---|
| `0x0000`–`0x0001` | 1–2 | Voltage scaling, loaded internally | 3, 8, 25 |
| `0x0002`–`0x0003` | 3–4 | Current scaling, loaded internally | 3, 8 |
| `0x0004` | 5 | Software version defined in RegisterMap, not exposed by a controller group | 3, 8 |
| `0x001B` | 28 | SolarArray: array voltage | 3, 9 |
| `0x001D` | 30 | SolarArray: array current | 3, 9 |
| `0x0023` | 36 | ChargeController: heatsink temperature | 3, 10 |
| `0x0025` | 38 | Battery: battery temperature | 3, 10 |
| `0x0026` | 39 | Battery: slow filtered battery voltage | 3, 10–11 |
| `0x0027` | 40 | Battery: slow filtered charging current | 3, 10–11 |
| `0x0031` | 50 | ChargeController: numeric LED state | 3, 12–13 |
| `0x0032` | 51 | ChargeController: numeric charge state | 3, 13 |
| `0x0033` | 52 | Battery: target regulation voltage | 3, 14 |
| `0x0034`–`0x0035` | 53–54 | ChargeController: resettable charge Ah | 4, 14 |
| `0x0038` | 57 | ChargeController: resettable charge kWh | 4, 14 |
| `0x003A` | 59 | Battery: output power | 4, 14 |
| `0x003C` | 61 | SolarArray: last sweep maximum power | 4, 14–15 |
| `0x003D` | 62 | SolarArray: last sweep Vmp | 4, 15 |
| `0x003E` | 63 | SolarArray: last sweep Voc | 4, 15 |

The controller groups and register definitions are in `src/tsmppt60_driver/controller/`
and `src/tsmppt60_driver/hal/register/_map.py`. The software-version constant is
not an exposed read path. Defining a register is not the same as exposing it through
`TsMppt60.get()`.

## Behavior and limitations to verify separately

- The driver sends HTTP requests to `MBCSV.cgi` with `ID=1` and `F=4`. This is
  a web CGI interface, not a direct Modbus TCP or serial implementation; the PDF
  describes Modbus rather than this CGI transport. ID 1 is a documented default,
  not a specification requirement that IDs cannot change.
- Every one-word read is currently converted as signed 16-bit, including kWh,
  output power and state values whose PDF signed cells are blank. Two-word reads
  are combined as unsigned HI then LO. See [signedness](scaling.md#signedness).
  This mismatch in interpretation needs separate investigation; no driver change
  or claim of device failure is made here.
- The driver exposes numeric LED and charge states without translating them. The
  source enumerations appear in [RAM registers](ram-registers.md#state-values).
- The driver rounds scaled values to two decimal places. It has no BCD conversion
  path for its defined software-version register.
- Solar input current may differ from actual input current by ±20%; input power
  may also have significant error (PDF pages 9 and 14).
