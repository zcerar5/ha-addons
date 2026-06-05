from importlib.util import find_spec
from pathlib import Path


WRITABLE_FALLBACK = """        if not writable_dids:
            try:
                from open3e.web.ha_discovery import WRITABLE_ENTITIES
                for key, cfg in WRITABLE_ENTITIES.items():
                    raw_did = cfg.get("did", key) if isinstance(cfg, dict) else key
                    try:
                        did = int(raw_did)
                    except (TypeError, ValueError):
                        continue
                    writable_dids.setdefault(did, cfg)
            except Exception:
                pass

"""


server_spec = find_spec("open3e.web.server")
if server_spec is None or server_spec.origin is None:
    raise RuntimeError("open3e.web.server was not found")

server_path = Path(server_spec.origin)
server_source = server_path.read_text()

anchor = """        # Get codec metadata for each writable DID
        try:
            import open3e.Open3Edatapoints as dp_mod
"""

if "from open3e.web.ha_discovery import WRITABLE_ENTITIES" not in server_source:
    if anchor not in server_source:
        raise RuntimeError("Could not find writable metadata anchor in server.py")
    server_source = server_source.replace(anchor, WRITABLE_FALLBACK + anchor, 1)
    server_path.write_text(server_source)
