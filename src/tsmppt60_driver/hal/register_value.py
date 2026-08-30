from dataclasses import dataclass
from typing import Self

from .base import DataClassBase


@dataclass(frozen=True, kw_only=True)
class RegisterValue(DataClassBase):
    """Represent a raw ModBus response and its register values."""

    mb_id: int
    field: int
    values: list[int]

    @classmethod
    def new(cls, raw: str) -> Self:
        """Create an instance from a comma-separated ModBus response."""
        [mb_id, field, length, *values] = [int(v) for v in raw.split(",")]
        if length != len(values):
            raise ValueError(f"Invalid {length=} with {values=}")

        return cls(
            mb_id=mb_id,
            field=field,
            values=values,
        )
