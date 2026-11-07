from ..register import Register, RegisterMap
from ._base import ModBusBase


class ModBusScaler(ModBusBase):
    """Read the voltage and current scale factors from the device."""

    def __init__(self, host: str, port: int, *, cgi: str = "MBCSV.cgi", timeout: int = 5, debug: bool = False):
        """Initialize a scaler reader for a TS-MPPT-60."""
        super().__init__(host, port, cgi, timeout, debug=debug)

    def _get_scaler(self, reg: Register) -> float:
        """Calculate a scale factor from a scaling register.

        The scale factor is represented as an integer part and a fractional
        part, where the fractional part is divided by ``2**16``.

        Args:
            reg: Scaling register to read.
        Returns:
            The calculated scale factor.
        """
        values = self._get_register_values(reg.address, reg.registers)
        return float(values[0]) + (float(values[1]) / pow(2, self.BITS_PER_REGISTER))

    def get_voltage_scaler(self) -> float:
        """Return the voltage scale factor."""
        return self._get_scaler(RegisterMap.VOLTAGE_SCALING)

    def get_current_scaler(self) -> float:
        """Return the current scale factor."""
        return self._get_scaler(RegisterMap.CURRENT_SCALING)
