from dataclasses import dataclass, field
from typing import Self

from ._base import RegisterBase


@dataclass(frozen=True, kw_only=True)
class Register(RegisterBase):
    """Describe a contiguous range of ModBus registers."""

    address: int
    registers: int
    label: str = field(default="")
    scale_factor: str = field(default="")


@dataclass(frozen=True, kw_only=True)
class RegisterValue(RegisterBase):
    """Represent a raw ModBus response and its register values."""

    mb_id: int
    field: int
    values: list[int]

    @classmethod
    def new(cls, raw: str) -> Self:
        """Create an instance from a comma-separated ModBus response."""
        [mb_id, field_, length, *values] = [int(v) for v in raw.split(",")]
        if length != len(values):
            raise ValueError(f"Invalid {length=} with {values=}")

        return cls(
            mb_id=mb_id,
            field=field_,
            values=values,
        )
