from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class Register:
    """MODBUS register value"""

    address: int
    registers: int
    label: str = field(default="")
    scale_factor: str = field(default="")


@dataclass(frozen=True)
class RegisterMap:
    """MODBUS register table for TS-MPPT-60 written on data sheet TSMPPT.APP_.Modbus.EN_.10.2.pdf."""

    VOLTAGE_SCALING = Register(address=0x0000, registers=2, label="Voltage Scaling")
    CURRENT_SCALING = Register(address=0x0002, registers=2, label="Current Scaling")
    SOFTWARE_VERSION = Register(address=0x0004, registers=1, label="Software Version", scale_factor="Numbers")
    ARRAY_VOLTAGE = Register(address=0x001B, registers=1, label="Array Voltage", scale_factor="V")
    ARRAY_CURRENT = Register(address=0x001D, registers=1, label="Array Current", scale_factor="A")
    HEATSINK_TEMP = Register(address=0x0023, registers=1, label="Heat Sink Temperature", scale_factor="C")
    BATTERY_TEMP = Register(address=0x0025, registers=1, label="Battery Temperature", scale_factor="C")
    BATTERY_VOLTAGE = Register(address=0x0026, registers=1, label="Battery Voltage", scale_factor="V")
    CHARGING_CURRENT = Register(address=0x0027, registers=1, label="Charge Current", scale_factor="A")
    LED_STATE = Register(address=0x0031, registers=1, label="LED State", scale_factor="Numbers")
    CHARGE_STATE = Register(address=0x0032, registers=1, label="Charge State", scale_factor="Numbers")
    TARGET_REGULATION_VOLTAGE = Register(address=0x0033, registers=1, label="Target Voltage", scale_factor="V")
    AH_CHARGE_RESETABLE = Register(address=0x0034, registers=2, label="Amp Hours", scale_factor="Ah")
    OUTPUT_POWER = Register(address=0x003A, registers=1, label="Output Power", scale_factor="W")
    VMP_LAST_SWEEP = Register(address=0x003D, registers=1, label="Sweep Vmp", scale_factor="V")
    VOC_LAST_SWEEP = Register(address=0x003E, registers=1, label="Sweep Voc", scale_factor="V")
    POWER_LAST_SWEEP = Register(address=0x003C, registers=1, label="Sweep Pmax", scale_factor="W")
    KWH_CHARGE_RESETABLE = Register(address=0x0038, registers=1, label="Kilowatt Hours", scale_factor="kWh")
