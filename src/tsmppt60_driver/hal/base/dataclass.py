from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class DataClassBase:
    """Base class for immutable data classes in the HAL."""

    def as_dict(self) -> dict[str, Any]:
        """Return the data class fields as a dictionary."""
        return asdict(self)
