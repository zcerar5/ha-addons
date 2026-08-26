"""Flatten O3ESwitch ZigBee payloads for Home Assistant compatibility.

Upstream's O3ESwitch codec nests the device-type dependent fields (e.g.
ActualTemperature, Humidity) inside the "ViCareDevice" object. The Open3e
HA integration and MQTT discovery consumers expect those fields at the top
level of the DID payload, as published by the previous codec. This patch
lifts the nested fields back to the top level before publishing and keeps
"ViCareDevice" as the plain {ID, Text} enum.
"""

from importlib.util import find_spec
from pathlib import Path


ANCHOR = "        value,idstr,idid =  dicEcus[addr].readByDid(did, raw, sub)\n"

FLATTEN = """        value = _flatten_vicare_device(value)
"""

HELPER = '''

def _flatten_vicare_device(value):
    """Lift O3ESwitch case fields out of ViCareDevice to the payload top level."""
    if isinstance(value, dict) and isinstance(value.get("ViCareDevice"), dict):
        vcd = value["ViCareDevice"]
        value = dict(value)
        value.update({k: v for k, v in vcd.items() if k not in ("ID", "Text")})
        value["ViCareDevice"] = {k: vcd[k] for k in ("ID", "Text") if k in vcd}
    return value

'''

spec = find_spec("open3e.Open3Eclient")
if spec is None or spec.origin is None:
    raise RuntimeError("open3e.Open3Eclient was not found")

path = Path(spec.origin)
source = path.read_text()

if "_flatten_vicare_device" not in source:
    if ANCHOR not in source:
        raise RuntimeError("Could not find readByDid anchor in Open3Eclient.py")

    import_anchor = "import json\n"
    if import_anchor not in source:
        raise RuntimeError("Could not find import anchor in Open3Eclient.py")

    source = source.replace(import_anchor, import_anchor + HELPER, 1)
    source = source.replace(ANCHOR, ANCHOR + FLATTEN, 1)
    path.write_text(source)
