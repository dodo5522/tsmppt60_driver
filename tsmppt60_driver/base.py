import logging

import requests


"""TS-MPPT-60 driver's base modules."""


class Logger(object):
    """Logger base class for this module."""

    _FORMAT_LOG_MSG = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    _FORMAT_LOG_DATE = "%Y/%m/%d %p %l:%M:%S"

    def __init__(self, log_file_path=None, debug=False):
        """Initialize Logger class object.

        Keyword arguments:
        log_file_path -- Path to record log file.
        debug -- If True, logging is enabled.
        """
        self.logger = logging.getLogger(type(self).__name__)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt=self._FORMAT_LOG_MSG, datefmt=self._FORMAT_LOG_DATE)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if log_file_path:
            handler = logging.FileHandler(log_file_path, mode="a")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)


class ModbusRegisterTable(object):
    """MODBUS register settings table."""

    VOLTAGE_SCALING_HIGH = (0x0000, "", "Voltage Scaling High", 1)
    VOLTAGE_SCALING_LOW = (0x0001, "", "Voltage Scaling Low", 1)
    CURRENT_SCALING_HIGH = (0x0002, "", "Current Scaling High", 1)
    CURRENT_SCALING_LOW = (0x0003, "", "Current Scaling Low", 1)
    VOLTAGE_SCALING = (0x0000, "", "Voltage Scaling", 2)
    CURRENT_SCALING = (0x0002, "", "Current Scaling", 2)
    SOFTWARE_VERSION = (0x0004, "Numbers", "Software Version", 1)

    BATTERY_VOLTAGE = (0x0026, "V", "Battery Voltage", 1)
    CHARGING_CURRENT = (0x0027, "A", "Charge Current", 1)
    TARGET_REGULATION_VOLTAGE = (0x0033, "V", "Target Voltage", 1)
    OUTPUT_POWER = (0x003A, "W", "Output Power", 1)
    ARRAY_VOLTAGE = (0x001B, "V", "Array Voltage", 1)
    ARRAY_CURRENT = (0x001D, "A", "Array Current", 1)
    VMP_LAST_SWEEP = (0x003D, "V", "Sweep Vmp", 1)
    VOC_LAST_SWEEP = (0x003E, "V", "Sweep Voc", 1)
    POWER_LAST_SWEEP = (0x003C, "W", "Sweep Pmax", 1)
    HEATSINK_TEMP = (0x0023, "C", "Heat Sink Temperature", 1)
    BATTERY_TEMP = (0x0025, "C", "Battery Temperature", 1)
    AH_CHARGE_RESETABLE = (0x0034, "Ah", "Amp Hours", 2)
    KWH_CHARGE_RESETABLE = (0x0038, "kWh", "Kilowatt Hours", 1)

    LED_STATE = (0x0031, "Numbers", "LED State", 1)
    CHARGE_STATE = (0x0032, "Numbers", "Charge State", 1)


class ManagementBase(object):
    """Class to get raw data from TS-MPPT-60. MODBUS ID is fixed to 1 as written on data sheet TSMPPT.APP_.Modbus.EN_.10.2.pdf.

    Keyword arguments:
    host -- host name like dummy.co.jp
    cgi -- cgi script file name
    debug -- debug message output is enabled if True
    """

    _ID_MODBUS = 0x01

    def __init__(self, host, cgi="MBCSV.cgi", debug=False):
        """Initialize class object.

        Keyword arguments:
        host -- Host address like "192.168.1.20" of TS-MPPT-60 live view
        cgi -- CGI file name to get the information
        debug -- If True, logging is enabled.
        """
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(logging.StreamHandler())

        if debug:
            self._logger.setLevel(logging.DEBUG)

        self._url = "http://" + host + "/" + cgi
        self._vscale = self._compute_scaler(ModbusRegisterTable.VOLTAGE_SCALING)
        self._iscale = self._compute_scaler(ModbusRegisterTable.CURRENT_SCALING)

    def _get(self, addr, reg, mbid=_ID_MODBUS, field=4):
        """Get and return raw data string like "1,4,1,1,1" against MBID, Address, Register, and Field.

        Keyword arguments:
        addr -- Address to get information
        reg -- Register to get information
        mbid -- MBID
        field -- Field to get information

        >>> mb._get(addr=0x0000, reg=1)
        '1,4,2,0,0'
        >>> mb._get(addr=0x0001, reg=1)
        '1,4,2,0,0'
        """
        params = []
        params.append("ID=" + str(mbid))
        params.append("F=" + str(field))
        params.append("AHI=" + str(addr >> 8))
        params.append("ALO=" + str(addr & 255))
        params.append("RHI=" + str(reg >> 8))
        params.append("RLO=" + str(reg & 255))

        res = requests.get("{0}?{1}".format(self._url, "&".join(params)), timeout=(5, 15))

        return res.text

    def _read_modbus(self, address, register, mbid=_ID_MODBUS):
        """Read and return the value string with short integer (ex. 16bit value) against MBID, Address, and Register.

        Keyword arguments:
        address -- Address to get information
        register -- Register to get information
        mbid -- MBID

        >>> mb._read_modbus(0x0000, 1)
        [0]
        >>> mb._read_modbus(0x0001, 1)
        [0]
        """
        raw_value_str = self._get(address, register, mbid)
        raw_values = [int(v) for v in raw_value_str.split(",")]
        idx_max = raw_values[2]
        raw_values = raw_values[3:]
        idx = 0
        ret = []

        while idx < idx_max:
            ret_short = raw_values[idx] << 8
            idx += 1
            ret_short += raw_values[idx]
            idx += 1
            ret.append(ret_short)

        return ret

    def _compute_scaler(self, param):
        """Compute and return the voltage/current scaler as written on data sheet page 8 or 25.
        This will be called only once when initializing this object.

        Vscaling = whole.fraction = [V_PU hi].[V_PU lo]

        Example:
        Address:Value(hex):Variable Name
        V_PU HI byte:0x004E = 78
        V_PU LO byte:0x03A6 = 934

        V_PU lo must be shifted by 16 (divided by 2^16)
        and then added to V_PU hi Vscaling = 78 + 934/65536 = 78.01425

        Keyword arguments:
        param -- register to get a value
        >>> mb._compute_scaler(ModbusRegisterTable.VOLTAGE_SCALING)
        0.0
        >>> mb._compute_scaler(ModbusRegisterTable.CURRENT_SCALING)
        0.0
        """
        values = self._read_modbus(param[0], param[3])
        return float(values[0]) + (float(values[1]) / pow(2, 16))

    def get_raw_value(self, address, register):
        """Return a raw value against address got from TS-MPPT-60.

        Keyword arguments:
        address -- address to get a value
        register -- register to get a value

        Returns:
            Raw value as integer type.

        >>> mb.get_raw_value(0x0026, 1)
        0
        >>> mb.get_raw_value(0x0027, 1)
        0
        """
        values = self._read_modbus(address, register)

        if register > 1:
            raw_value = (values[0] << 16) | (values[1] & 0xFFFF)
        else:
            raw_value = values[0]
            raw_value &= 0xFFFF
            if raw_value & 0x8000:
                raw_value ^= 0xFFFF
                raw_value = -1 * (raw_value + 1)

        return raw_value

    def get_scaled_value(self, address, scale_factor, register):
        """Calculate and return a scaled status value against address got from TS-MPPT-60.

        Keyword arguments:
        address -- address to get a value
        scale_factor -- unit string
        register -- register to get a value

        Returns:
            Scaled value like 12.4 against your expecting.

        >>> mb.get_scaled_value(0x0026, "V", 1)
        0.0
        >>> mb.get_scaled_value(0x0027, "A", 1)
        0.0
        """
        raw_value = self.get_raw_value(address, register)

        if scale_factor == "V":
            scaled_value = raw_value * self._vscale / pow(2, 15)
        elif scale_factor == "A":
            scaled_value = raw_value * self._iscale / pow(2, 15)
        elif scale_factor == "W":
            wscale = self._iscale * self._vscale
            scaled_value = raw_value * wscale / pow(2, 17)
        elif scale_factor == "Ah":
            scaled_value = raw_value / 10.0
        else:
            scaled_value = raw_value

        return round(scaled_value, 2)


if __name__ == "__main__":
    import doctest

    try:
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    class DummyRequest(object):
        """Dummy response class against requests.Response."""

        pass

    class DummyResponse(object):
        """Dummy response class against requests.Response."""

        pass

    dummy_host = "dummy.co.jp"

    req = DummyRequest()
    req.url = "http://" + dummy_host + "/dummy.cgi"
    res = DummyResponse()
    res.request = req
    res.text = "1,4,2,0,0"

    with patch("requests.get", returns=res) as _m:
        _m.return_value = res
        doctest.testmod(verbose=True, extraglobs={"mb": ManagementBase(host=dummy_host)})
