---
type: Reference
title: TriStar MPPT Scaling and Word Order
description: Rules for converting Modbus register values to physical values
tags: [modbus, scaling, endian, registers]
sources:
  - id: tsmppt-v10.2
    resource: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
    title: TriStar MPPT MODBUS Specification V10.2
---

# Scaling

## V_PU and I_PU

`V_PU` is built from RAM `0x0000` (HI) and `0x0001` (LO). `I_PU` is built from RAM
`0x0002` (HI) and `0x0003` (LO).

```text
Vscaling = V_PU_hi + V_PU_lo / 2^16
Iscaling = I_PU_hi + I_PU_lo / 2^16
```

Most voltage values use `raw * Vscaling / 2^15`; most current values use
`raw * Iscaling / 2^15`. Percentage values use `raw * 100 / 2^16`.

Power values generally use `raw * Vscaling * Iscaling / 2^17`.

## Signedness

The RAM tables on PDF pages 3-4 have a `Signed` column. Page 26 records that
this column was added in revision V08. A check mark explicitly identifies a signed
value; it is not limited to temperature registers. In particular, the voltage and
current measurements at `0x0018`-`0x001D`, slow measurements and extrema at
`0x0026`-`0x0029`, and target voltage at `0x0033` are checked.

The hourmeter (`0x002A`/`0x002B`), alarm bitfield (`0x002E`/`0x002F`), and
charge-Ah counters (`0x0034`-`0x0037`) have blank `Signed` cells. Reading these
as unsigned combined values is the interpretation used by this bundle. The PDF
has no explicit legend defining a blank cell, so this interpretation must not be
presented as a verbatim unsigned declaration. Register count alone does not
determine signedness.

`registers.json` preserves the evidence in `signed_column` (`checked` or `blank`)
and identifies the printed PDF page with `source_page`. Checked entries also have
`signed: true`. An omitted `signed` field alone is not evidence of unsigned data;
consult `signed_column` and the source. This distinction also applies to one-word
power values, whose `Signed` cells are blank on page 4.

For a 16-bit two's-complement interpretation, boundary examples are
`0x0000 -> 0`, `0x7FFF -> 32767`, `0x8000 -> -32768`, and `0xFFFF -> -1`.
For an unsigned two-word value, `HI=0xFFFF`, `LO=0xFFFF` combines to
`4294967295`, without sign conversion. These are decoding examples, not claims
about the attainable measurement range of a particular register.

## Multi-word values

The specification's page-25 example uses LO `0x002A` and HI `0x002B`:

```text
value = (HI << 16) | LO
```

However, the register table lists `0x002A` as HI and `0x002B` as LO. This source inconsistency
is documented in `ram-registers.md`; verify the hourmeter word order on the target device.

The charge-Ah pairs at `0x0034`/`0x0035` and `0x0036`/`0x0037` are HI/LO
in the page-4 table. Combine the words first, then multiply the combined value by
`0.1` to obtain Ah. Their descriptions are on page 14. Do not apply `0.1`
independently to each word. The kWh counters at `0x0038` and `0x0039` are
separate one-word counters, not a HI/LO pair.

The page-25 hourmeter example combines `HI=0x0022` and `LO=0x13D8` into
`0x002213D8` (2,233,304 hours). Its top bit is clear, so the example cannot
establish signed versus unsigned behavior at the 32-bit boundary.

## Example

With `V_PU_hi=0x007B`, `V_PU_lo=0xE041`, and battery raw=`0x0DB0`,
`Vscaling=123.876` and the battery voltage is approximately 13.25 V.
