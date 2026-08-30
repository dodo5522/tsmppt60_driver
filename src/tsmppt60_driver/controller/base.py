import logging
from typing import Sequence

from ..hal import ModBus, Register


class ControllerBase:
    """Base class for controllers that read status data from a ModBus device."""

    def __init__(self, mb: ModBus, group: str, registers: list[Register], *, debug: bool = False):
        """Initialize a controller.

        Args:
            mb: ModBus instance used to read register values.
            group: Name of the controller group.
            registers: Registers exposed by this controller.
            debug: Enable debug logging when ``True``.
        """
        self._mb = mb
        self._group = group
        self._registers = registers

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", "%Y/%m/%d %p %l:%M:%S")
        )

        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(handler)

        if debug:
            self._logger.setLevel(logging.DEBUG)

    def __repr__(self):
        """Return the controller group name for debugging and display."""
        return self._group

    def __str__(self):
        """Return the controller group name."""
        return self._group

    @property
    def group(self) -> str:
        """Return the controller group name."""
        return self._group

    @property
    def labels(self) -> set[str]:
        """Return the labels exposed by this controller."""
        return {r.label for r in self._registers}

    def get(self, *, target_labels: Sequence[str] | None = None):
        """Return status data for the selected labels.

        If ``target_labels`` is omitted, all labels exposed by this controller
        are read. The result is nested under the controller's group name.

        Args:
            target_labels: Labels to include in the result.

        Returns:
            A nested dictionary containing the selected status data.
        """
        if target_labels is None:
            target_labels = self.labels

        return {
            self.group: {
                r.label: {
                    "value": self._mb.get_scaled_value(r.address, r.scale_factor, r.registers),
                    "unit": r.scale_factor,
                }
                for r in self._registers
                if r.label in target_labels
            }
        }
