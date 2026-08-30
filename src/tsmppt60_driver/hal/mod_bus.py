import logging
from http.client import HTTPConnection
from time import sleep

from .register import Register, RegisterMap
from .register_value import RegisterValue


"""
TS-MPPT-60 driver's base modules.
"""


class ModBusBase:
    def __init__(self, host: str, port: int, cgi: str, timeout: int, *, debug: bool = False):
        """Base class to get raw data from TS-MPPT-60. MODBUS ID is fixed to 1 as written on data sheet TSMPPT.APP_.Modbus.EN_.10.2.pdf.

        Args:
            host: Host address like "192.168.1.20" of TS-MPPT-60 live view
            port: Port number like 80 of TS-MPPT-60 live view
            cgi: CGI file name to get the information
            timeout: Connection timeout seconds
        Keyword Args:
            debug: If True, logging is enabled.
        """
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(logging.StreamHandler())

        if debug:
            self._logger.setLevel(logging.DEBUG)

        self._connection = HTTPConnection(host, port=port, timeout=timeout)
        self._endpoint = f"/{cgi}"

    def _get(self, params: list[str], *, retries: int = 3, initial_wait: int = 1) -> str:
        """Get response from the specified TS-MPPT-60.

        Args:
            params: Query parameters list like ["ID=1", "F=..."]
        Keyword Args:
            retries: Max retry if failed to get
            initial_wait: Initial wait time of second if failed to get
        Returns:
            Read modbus response string
        """
        read_text = ""
        wait_sec = initial_wait

        while retries:
            self._connection.request("GET", f"{self._endpoint}?{'&'.join(params)}")
            response = self._connection.getresponse()

            if response.status != 200:
                sleep(wait_sec)
                retries -= 1
                wait_sec *= 2
                continue

            read_text = response.read().decode("ASCII")
            break

        return read_text

    def _get_register_values(self, address: int, registers: int) -> tuple[int, ...]:
        """Read values with short integer (ex. 16bit value) against MBID, Address, and Register.

        Args:
            address: Address to get information
            registers: Register to get information
        Returns:
            Integer part (HI value) and fractional part (LO value) if got 2 values.
            Integer value if got a value.

        >>> mb._get_register_values(0x0000, 1)
        (0, 0)
        """
        mod_bus_id = 1
        field = 4

        reg = RegisterValue.new(
            self._get(
                [
                    f"ID={mod_bus_id}",
                    f"F={field}",
                    f"AHI={address >> 8}",
                    f"ALO={address & 255}",
                    f"RHI={registers >> 8}",
                    f"RLO={registers & 255}",
                ]
            )
        )
        short_values = []

        idx = 0
        while idx < len(reg.values):
            short_value = reg.values[idx] << 8
            idx += 1
            short_value += reg.values[idx]
            idx += 1
            short_values.append(short_value)

        return tuple(short_values)


class ModBusScaler(ModBusBase):
    def __init__(self, host: str, port: int, *, cgi: str = "MBCSV.cgi", timeout: int = 5, debug: bool = False):
        super().__init__(host, port, cgi, timeout, debug=debug)

    def _get_scaler(self, reg: Register) -> float:
        """Compute and return the voltage/current scaler as written on data sheet page 8 or 25.
        This will be called only once when initializing this object.

        Vscaling = whole.fraction = [V_PU hi].[V_PU lo]

        Example:
        Address:Value(hex):Variable Name
        V_PU HI byte:0x004E = 78
        V_PU LO byte:0x03A6 = 934

        V_PU lo must be shifted by 16 (divided by 2^16)
        and then added to V_PU hi Vscaling = 78 + 934/65536 = 78.01425

        Keyword Args:
            reg: register to get a value
        Returns:
            Computed value

        >>> mb_scaler._get_scaler(RegisterMap.VOLTAGE_SCALING)
        0.0
        >>> mb_scaler._get_scaler(RegisterMap.CURRENT_SCALING)
        0.0
        """
        values = self._get_register_values(reg.address, reg.registers)
        return float(values[0]) + (float(values[1]) / pow(2, 16))

    def get_voltage_scaler(self) -> float:
        return self._get_scaler(RegisterMap.VOLTAGE_SCALING)

    def get_current_scaler(self) -> float:
        return self._get_scaler(RegisterMap.CURRENT_SCALING)


class ModBus(ModBusBase):
    def __init__(self, host: str, port: int, *, cgi: str = "MBCSV.cgi", timeout: int = 5, debug: bool = False):
        super().__init__(host, port, cgi, timeout, debug=debug)

        scaler = ModBusScaler(host, port, cgi=cgi, timeout=timeout, debug=debug)
        self._voltage_scale = scaler.get_voltage_scaler()
        self._current_scale = scaler.get_current_scaler()

    def get_value(self, address: int, register: int):
        """Return a raw value against address got from TS-MPPT-60.

        Args:
            address: address to get a value
            register: register to get a value
        Returns:
            Raw value as integer type.

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
        """Calculate and return a scaled status value against address got from TS-MPPT-60.

        Args:
            address: address to get a value
            scale_factor: unit string
            register: register to get a value
        Returns:
            Scaled value like 12.4 against your expecting.

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
