from importlib.util import find_spec
from pathlib import Path


ROOM_CURRENT_VALUE_DIDS = (
    *range(2086, 2144, 3),
    *range(2262, 2320, 3),
)

spec = find_spec("open3e.Open3EdatapointsVdens")
if spec is None or spec.origin is None:
    raise RuntimeError("Open3EdatapointsVdens.py was not found")

path = Path(spec.origin)
source = path.read_text()

if "variantDataIdentifiers" not in source:
    imports = "from open3e.Open3Ecodecs import *\n\n"
    if imports not in source:
        raise RuntimeError("Could not find Open3EdatapointsVdens import anchor")

    source = source.replace(
        imports,
        "from open3e.Open3Ecodecs import *\n"
        "from open3e.Open3EdatapointsVariants import dataIdentifiers as variantDataIdentifiers\n\n\n"
        "def _variant_did(did: int, length: int):\n"
        "    return variantDataIdentifiers[\"dids\"][did][length]\n\n",
        1,
    )

if "2319 : _variant_did(2319, 68)" not in source:
    did_anchor = "        1800 : None,\n"
    if did_anchor not in source:
        raise RuntimeError("Could not find Open3EdatapointsVdens DID anchor")

    room_dids = "".join(
        f"        {did} : _variant_did({did}, 68),\n"
        for did in ROOM_CURRENT_VALUE_DIDS
    )
    source = source.replace(did_anchor, did_anchor + room_dids, 1)

path.write_text(source)
