from .base import ModBusBase
from .register import Register, RegisterMap


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

        >>> mb_scaler._get_scaler(RegisterMap.VOLTAGE_SCALING)
        0.0
        >>> mb_scaler._get_scaler(RegisterMap.CURRENT_SCALING)
        0.0
        """
        values = self._get_register_values(reg.address, reg.registers)
        return float(values[0]) + (float(values[1]) / pow(2, 16))

    def get_voltage_scaler(self) -> float:
        """Return the voltage scale factor."""
        return self._get_scaler(RegisterMap.VOLTAGE_SCALING)

    def get_current_scaler(self) -> float:
        """Return the current scale factor."""
        return self._get_scaler(RegisterMap.CURRENT_SCALING)


class ModBus(ModBusBase):
    """Read raw and scaled values from the TS-MPPT-60."""

    def __init__(self, host: str, port: int, *, cgi: str = "MBCSV.cgi", timeout: int = 5, debug: bool = False):
        """Initialize a ModBus reader and load its voltage/current scales."""
        super().__init__(host, port, cgi, timeout, debug=debug)

        scaler = ModBusScaler(host, port, cgi=cgi, timeout=timeout, debug=debug)
        self._voltage_scale = scaler.get_voltage_scaler()
        self._current_scale = scaler.get_current_scaler()

    def get_value(self, address: int, register: int):
        """Return the raw value stored at a register address.

        Args:
            address: Starting register address.
            register: Number of registers to read.
        Returns:
            The raw register value as an integer.

        >>> mb.get_value(0x0026, 1)
        0
        >>> mb.get_value(0x0027, 1)
        0
        """
        values = self._get_register_values(address, register)

        if register > 1:
            raw_value = (values[0] << 16) | (values[1] & 0xFFFF)
        else:
            raw_value = values[0]
            raw_value &= 0xFFFF
            if raw_value & 0x8000:
                raw_value ^= 0xFFFF
                raw_value = -1 * (raw_value + 1)

        return raw_value

    def get_scaled_value(self, address: int, scale_factor: str, register: int) -> float:
        """Return a raw register value converted to the requested unit.

        Args:
            address: Starting register address.
            scale_factor: Unit or scale-factor identifier, such as ``"V"``.
            register: Number of registers to read.
        Returns:
            The rounded, scaled value.

        >>> mb.get_scaled_value(0x0026, "V", 1)
        0.0
        >>> mb.get_scaled_value(0x0027, "A", 1)
        0.0
        """
        raw_value = self.get_value(address, register)

        if scale_factor == "V":
            scaled_value = raw_value * self._voltage_scale / pow(2, 15)
        elif scale_factor == "A":
            scaled_value = raw_value * self._current_scale / pow(2, 15)
        elif scale_factor == "W":
            wscale = self._current_scale * self._voltage_scale
            scaled_value = raw_value * wscale / pow(2, 17)
        elif scale_factor == "Ah":
            scaled_value = raw_value / 10.0
        else:
            scaled_value = raw_value

        return round(scaled_value, 2)


if __name__ == "__main__":
    import doctest
    from unittest.mock import patch

    with patch.object(ModBusBase, "_get", return_value="1,4,4,0,0,0,0"):
        doctest.testmod(
            verbose=True,
            extraglobs={
                "mb": ModBus(host="dummy.com", port=80),
                "mb_scaler": ModBusScaler(host="dummy.com", port=80),
            },
        )
