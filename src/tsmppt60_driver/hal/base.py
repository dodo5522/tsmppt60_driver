from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class BaseClass:
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
