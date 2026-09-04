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

## Multi-word values

The specification's page-25 example uses LO `0x002A` and HI `0x002B`:

```text
value = (HI << 16) | LO
```

However, the register table lists `0x002A` as HI and `0x002B` as LO. This source inconsistency
is documented in `ram-registers.md`; verify the hourmeter word order on the target device.

## Example

With `V_PU_hi=0x007B`, `V_PU_lo=0xE041`, and battery raw=`0x0DB0`,
`Vscaling=123.876` and the battery voltage is approximately 13.25 V.
