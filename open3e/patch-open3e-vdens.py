from importlib.util import find_spec
from pathlib import Path


ROOM_CURRENT_VALUE_DIDS = (
    *range(2086, 2144, 3),
    *range(2262, 2320, 3),
)


def _patch_profile(module_name: str, did_anchor: str, use_variant_codec: bool):
    spec = find_spec(f"open3e.{module_name}")
    if spec is None or spec.origin is None:
        raise RuntimeError(f"{module_name}.py was not found")

    path = Path(spec.origin)
    source = path.read_text()

    if use_variant_codec and "variantDataIdentifiers" not in source:
        imports = "from open3e.Open3Ecodecs import *\n\n"
        if imports not in source:
            raise RuntimeError(f"Could not find {module_name} import anchor")

        source = source.replace(
            imports,
            "from open3e.Open3Ecodecs import *\n"
            "from open3e.Open3EdatapointsVariants import dataIdentifiers as variantDataIdentifiers\n\n\n"
            "def _variant_did(did: int, length: int):\n"
            "    return variantDataIdentifiers[\"dids\"][did][length]\n\n",
            1,
        )

    if "2319 : " not in source:
        if use_variant_codec:
            room_dids = "".join(
                f"        {did} : _variant_did({did}, 68),\n"
                for did in ROOM_CURRENT_VALUE_DIDS
            )
        else:
            room_dids = "".join(
                f"        {did} : None,\n"
                for did in ROOM_CURRENT_VALUE_DIDS
            )

        source = source.replace(did_anchor, did_anchor + room_dids, 1)

    path.write_text(source)


for profile in (
    ("Open3EdatapointsVcal", "        1844 : None,\n", False),
    ("Open3EdatapointsVdens", "        1800 : None,\n", True),
):
    _, did_anchor, _ = profile
    spec = find_spec(f"open3e.{profile[0]}")
    if spec is None or spec.origin is None:
        raise RuntimeError(f"{profile[0]}.py was not found")
    if did_anchor not in Path(spec.origin).read_text():
        raise RuntimeError(f"Could not find {profile[0]} DID anchor")

    _patch_profile(*profile)
