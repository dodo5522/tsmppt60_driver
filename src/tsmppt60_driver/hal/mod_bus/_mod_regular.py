from ._base import ModBusBase
from ._mod_scaler import ModBusScaler


def _as_two_complement(raw_value: int, bits: int) -> int:
    """Calculate the raw value with two complementary bits.

    Args:
        raw_value: Raw register value
        bits: Number of bits
    Returns:
        Positive or negative value
    """
    mask = 2**bits - 1
    sign_mask = 2 ** (bits - 1)

    value = raw_value
    value &= mask
    if value & sign_mask:
        value ^= mask
        value = -1 * (value + 1)

    return value


class ModBus(ModBusBase):
    """Read raw and scaled values from the TS-MPPT-60."""

    def __init__(self, host: str, port: int, *, cgi: str = "MBCSV.cgi", timeout: int = 5, debug: bool = False):
        """Initialize a ModBus reader and load its voltage/current scales."""
        super().__init__(host, port, cgi, timeout, debug=debug)

        scaler = ModBusScaler(host, port, cgi=cgi, timeout=timeout, debug=debug)
        self._voltage_scale = scaler.get_voltage_scaler()
        self._current_scale = scaler.get_current_scaler()

    def get_value(self, address: int, register: int) -> int:
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
        raw_values = self._get_register_values(address, register)

        match register:
            case 1:
                value = _as_two_complement(raw_values[0], 16)
            case 2:
                value = _as_two_complement((raw_values[0] << self.BITS_PER_REGISTER) | raw_values[1], 32)
            case _:
                raise ValueError("Invalid register number")

        return value

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
