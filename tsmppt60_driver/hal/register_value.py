from dataclasses import dataclass
from typing import Self

from tsmppt60_driver.hal.base import BaseClass


@dataclass(frozen=True, kw_only=True)
class RegisterValue(BaseClass):
    """MODBUS register value"""

    mb_id: int
    field: int
    values: list[int]

    @classmethod
    def new(cls, raw: str) -> Self:
        [mb_id, field, length, *values] = [int(v) for v in raw.split(",")]
        if length != len(values):
            raise ValueError(f"Invalid {length=} with {values=}")

        return cls(
            mb_id=mb_id,
            field=field,
            values=values,
        )
