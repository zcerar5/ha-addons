from importlib.util import find_spec
from pathlib import Path


DEFAULT_DID_SETUP = """        hacs_default_dids = {
            265, 268, 269, 271, 274, 284, 286, 288, 290, 318, 320, 321, 322, 324,
            325, 327, 328, 329, 330, 331, 334, 335, 336, 337, 355, 360, 364, 381,
            389, 391, 396, 401, 402, 403, 404, 419, 420, 421, 422, 424, 426, 428,
            430, 437, 439, 475, 476, 477, 478, 491, 497, 503, 505, 506, 522, 527,
            531, 533, 535, 543, 544, 545, 548, 565, 566, 593, 602, 607, 627, 628,
            629, 630, 873, 875, 876, 880, 881, 882, 883, 900, 901, 902, 927, 928,
            929, 987, 988, 989, 990, 1004, 1006, 1040, 1041, 1043, 1085, 1088,
            1089, 1100, 1101, 1102, 1103, 1104, 1105, 1165, 1192, 1193, 1211,
            1339, 1346, 1391, 1415, 1416, 1417, 1418, 1504, 1537, 1603, 1643,
            1644, 1664, 1684, 1690, 1731, 1769, 1771, 1772, 1775, 1776, 1801,
            1802, 1833, 1834, 1836, 1837, 1838, 2214, 2240, 2256, 2320, 2328,
            2333, 2334, 2346, 2350, 2351, 2352, 2369, 2370, 2371, 2403, 2405,
            2406, 2407, 2408, 2413, 2414, 2415, 2416, 2442, 2486, 2487, 2488,
            2489, 2496, 2529, 2543, 2544, 2545, 2546, 2547, 2548, 2549, 2560,
            2569, 2622, 2624, 2625, 2626, 2629, 2630, 2634, 2643, 2735, 2760,
            2791, 2792, 2793, 2797, 2806, 2855, 2856, 3016, 3017, 3018, 3029,
            3070, 3106, 3232, 3233, 3234,
        }
        mixer_room_sensor_dids = {334, 335, 336, 337}
        room_current_value_dids = (
            set(range(1886, 1944, 3)) |
            set(range(2086, 2144, 3)) |
            set(range(2262, 2320, 3))
        )
        room_dids = mixer_room_sensor_dids | room_current_value_dids
        default_dids = hacs_default_dids | room_dids
        mixer_room_fields = (
            ("Actual", "temperature", "\\u00b0C"),
            ("Minimum", "temperature", "\\u00b0C"),
            ("Maximum", "temperature", "\\u00b0C"),
            ("Average", "temperature", "\\u00b0C"),
        )
        room_current_value_fields = (
            ("ActualTemp", "temperature", "\\u00b0C"),
            ("MinimumTemp", "temperature", "\\u00b0C"),
            ("MaximumTemp", "temperature", "\\u00b0C"),
            ("ActualHumidity", "humidity", "%"),
            ("MinimumHumidity", "humidity", "%"),
            ("MaximumHumidity", "humidity", "%"),
        )

        datapoints = await store.get_datapoints()
        defaults_enabled = 0
        for dp in datapoints:
            if dp["did"] not in default_dids:
                continue
            updates = {}
            if not dp["poll_enabled"]:
                updates["poll_enabled"] = 1
            if dp["poll_priority"] <= 0:
                updates["poll_priority"] = 1
            if updates:
                await store.update_datapoint(dp["id"], **updates)
                defaults_enabled += 1

        if defaults_enabled:
            datapoints = await store.get_datapoints()
"""


ROOM_ENTITY_BLOCK = """            if dp["did"] in room_dids:
                ecu_hex = format(dp["ecu_address"], "03x")
                fields = mixer_room_fields if dp["did"] in mixer_room_sensor_dids else room_current_value_fields
                for sub_field, device_class, unit in fields:
                    unique_id = "o3e_{}_{}_{}".format(
                        ecu_hex, dp["did"], sub_field.lower()
                    )
                    base_name = _humanize(dp["name"])
                    field_label = _humanize(sub_field)
                    entity_name = base_name if field_label in base_name else base_name + " " + field_label
                    await store.upsert_ha_entity(
                        dp_id=dp["id"],
                        entity_type="sensor",
                        unique_id=unique_id,
                        name=entity_name,
                        device_class=device_class,
                        unit=unit,
                        enabled=1,
                        sub_field=sub_field,
                    )
                    created += 1
                continue

"""


SCHEDULE_RELOAD_BLOCK = """        engine = getattr(app.state, "engine", None)
        if engine and getattr(engine, "state", None) and engine.state.value == "polling":
            dp_rows = await store.get_datapoints()
            engine.send_command({
                "action": "update_schedule",
                "datapoints": {row["id"]: dict(row) for row in dp_rows},
            })

"""


server_spec = find_spec("open3e.web.server")
if server_spec is None or server_spec.origin is None:
    raise RuntimeError("open3e.web.server was not found")

server_path = Path(server_spec.origin)
server_source = server_path.read_text()

datapoint_anchor = """        # Only create HA entities for poll-enabled datapoints with priority > 0
        datapoints = await store.get_datapoints()
"""
if "hacs_default_dids = {" not in server_source:
    if datapoint_anchor not in server_source:
        raise RuntimeError("Could not find HA default datapoint anchor in server.py")
    server_source = server_source.replace(
        datapoint_anchor,
        "        # Select HACS-compatible defaults before creating HA discovery entities.\n" + DEFAULT_DID_SETUP,
        1,
    )

room_anchor = "        for dp in active_dps:\n"
if 'if dp["did"] in room_dids:' not in server_source:
    if room_anchor not in server_source:
        raise RuntimeError("Could not find HA entity loop anchor in server.py")
    server_source = server_source.replace(room_anchor, room_anchor + ROOM_ENTITY_BLOCK, 1)

return_anchor = '        return {"status": "ok", "entities_created": created}\n'
if '"datapoints_enabled": defaults_enabled' not in server_source:
    if return_anchor not in server_source:
        raise RuntimeError("Could not find HA defaults return anchor in server.py")
    server_source = server_source.replace(
        return_anchor,
        SCHEDULE_RELOAD_BLOCK +
        '        return {"status": "ok", "entities_created": created, "datapoints_enabled": defaults_enabled}\n',
        1,
    )

server_path.write_text(server_source)
