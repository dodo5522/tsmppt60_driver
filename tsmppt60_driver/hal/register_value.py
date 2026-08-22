from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class RegisterValue:
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
