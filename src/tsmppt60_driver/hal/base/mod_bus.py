import logging
from http.client import HTTPConnection
from time import sleep

from ..register_value import RegisterValue


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
