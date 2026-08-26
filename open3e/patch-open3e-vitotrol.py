"""Add ViCareDevice type 8 (Vitotrol room remote) to the ZigBee O3ESwitch codec.

Upstream's O3ESwitch only decodes device types 0-5, so a Vitotrol 300-E
(type 8) falls into the raw fallback and publishes no temperature or
humidity. Live capture on a Vitotrol 300-E (values cross-checked against
the device display: 24.4 degC / 64 %):

    offset 42-43: f4 00 -> int16 LE 244 -> 24.4 degC (same as climate sensor)
    offset 44:    00    -> unknown
    offset 45:    40    -> 64 % humidity (one byte later than climate sensor)

This patch adds case 8 with that layout to all ZigBee DeviceCurrentValues
switch definitions and names the type in the ViCareDeviceTypes enum.
"""

from importlib.util import find_spec
from pathlib import Path


SWITCH_ANCHOR = '{0: RawCodec(14, "Unknown_42_55"), 1:'

VITOTROL_CASE = (
    '{0: RawCodec(14, "Unknown_42_55"), '
    '8: O3EComplexType(14, "Data", ['
    'O3EInt16(2, "ActualTemperature", scale=10, unit="°C"), '
    'RawCodec(1, "Unknown_44"), '
    'O3EInt8(1, "Humidity", unit="%"), '
    'RawCodec(2, "Unknown_46_47"), '
    'RawCodec(1, "Unknown_48"), '
    'RawCodec(5, "Unknown_49_53"), '
    'RawCodec(1, "Unknown_54"), '
    'RawCodec(1, "Unknown_55")]), 1:'
)

ENUM_ANCHOR = '        7: "Repeater",\n'
ENUM_ADD = '        7: "Repeater",\n        8: "Vitotrol room remote",\n'


def patch_file(module_name, old, new, marker):
    spec = find_spec(module_name)
    if spec is None or spec.origin is None:
        raise RuntimeError("%s was not found" % module_name)
    path = Path(spec.origin)
    source = path.read_text()
    if marker in source:
        return 0
    count = source.count(old)
    if count == 0:
        raise RuntimeError("Anchor not found in %s" % module_name)
    path.write_text(source.replace(old, new))
    return count


n = patch_file("open3e.Open3EdatapointsVariants", SWITCH_ANCHOR, VITOTROL_CASE,
               '8: O3EComplexType(14, "Data"')
print("Vitotrol case added to %d switch definitions" % n)

n = patch_file("open3e.Open3Eenums", ENUM_ANCHOR, ENUM_ADD, '8: "Vitotrol')
print("enum entries added: %d" % n)
