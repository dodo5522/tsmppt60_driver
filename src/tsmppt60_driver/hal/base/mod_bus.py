import logging
from http.client import HTTPConnection
from time import sleep

from ..register_value import RegisterValue


class ModBusBase:
    """Provide the common HTTP and register-reading operations for ModBus."""

    def __init__(self, host: str, port: int, cgi: str, timeout: int, *, debug: bool = False):
        """Initialize a ModBus connection.

        The ModBus ID is fixed at 1 according to the TS-MPPT-60 ModBus
        specification.

        Args:
            host: Host address of the TS-MPPT-60 live view.
            port: Port number of the live view.
            cgi: CGI endpoint used to retrieve data.
            timeout: Connection timeout in seconds.
            debug: Enable debug logging when ``True``.
        """
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(logging.StreamHandler())

        if debug:
            self._logger.setLevel(logging.DEBUG)

        self._connection = HTTPConnection(host, port=port, timeout=timeout)
        self._endpoint = f"/{cgi}"

    def _get(self, params: list[str], *, retries: int = 3, initial_wait: int = 1) -> str:
        """Retrieve a raw response from the TS-MPPT-60.

        Args:
            params: Query parameters, such as ``["ID=1", "F=4"]``.
            retries: Maximum number of attempts after a failed request.
            initial_wait: Initial wait time in seconds before retrying.
        Returns:
            The response body, or an empty string if all attempts fail.
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
        """Read 16-bit register values from the device.

        Args:
            address: Starting register address.
            registers: Number of registers to read.
        Returns:
            A tuple containing the returned register bytes combined into
            unsigned 16-bit values.

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
