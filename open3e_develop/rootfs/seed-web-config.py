#!/usr/bin/env python3
"""Seed Open3e Web UI settings from Home Assistant add-on options."""

import os
import sqlite3

DEFAULT_MQTT_FORMAT = "{didNumber}_{didName}"
LEGACY_ADDON_MQTT_FORMAT = "{device}_{ecuAddr:03X}_{didNumber}_{didName}"
HACS_BASE_DIDS = (
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
)
MIXER_ROOM_SENSOR_DIDS = (334, 335, 336, 337)
ROOM_CURRENT_VALUE_DIDS = tuple(range(1886, 1944, 3))
ROOM_DIDS = MIXER_ROOM_SENSOR_DIDS + ROOM_CURRENT_VALUE_DIDS
ROOM_FIELDS = (
    ("ActualTemp", "temperature", "\u00b0C"),
    ("MinimumTemp", "temperature", "\u00b0C"),
    ("MaximumTemp", "temperature", "\u00b0C"),
    ("ActualHumidity", "humidity", "%"),
    ("MinimumHumidity", "humidity", "%"),
    ("MaximumHumidity", "humidity", "%"),
)
MIXER_FIELDS = (
    ("Actual", "temperature", "\u00b0C"),
    ("Minimum", "temperature", "\u00b0C"),
    ("Maximum", "temperature", "\u00b0C"),
    ("Average", "temperature", "\u00b0C"),
)


def set_setting(cursor, key, value):
    if value is None or value == "":
        return
    cursor.execute(
        """
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, str(value)),
    )


def bool_setting(value, default=False):
    if value is None or value == "":
        return "1" if default else "0"
    return "1" if str(value).lower() in ("1", "true", "yes", "on") else "0"


def table_exists(cursor, table):
    cursor.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table,),
    )
    return cursor.fetchone() is not None


def ensure_column(cursor, table, column, definition):
    cursor.execute("PRAGMA table_info({})".format(table))
    columns = {row[1] for row in cursor.fetchall()}
    if column not in columns:
        cursor.execute(
            "ALTER TABLE {} ADD COLUMN {} {}".format(table, column, definition)
        )


def humanize(name):
    parts = []
    current = ""
    for char in name:
        if current and char.isupper() and not current[-1].isupper():
            parts.append(current)
            current = char
        else:
            current += char
    if current:
        parts.append(current)
    return " ".join(parts)


def apply_room_datapoint_preset(cursor):
    if not table_exists(cursor, "datapoints"):
        return

    placeholders = ",".join("?" for _ in ROOM_DIDS)
    cursor.execute(
        """
        UPDATE datapoints
        SET poll_enabled = 1,
            poll_priority = 1
        WHERE did IN ({})
          AND poll_enabled = 0
          AND poll_priority = 0
        """.format(placeholders),
        ROOM_DIDS,
    )

    if not table_exists(cursor, "ha_entities"):
        return

    ensure_column(cursor, "ha_entities", "sub_field", "TEXT")
    cursor.execute(
        """
        SELECT id, ecu_address, did, name
        FROM datapoints
        WHERE did IN ({})
        """.format(placeholders),
        ROOM_DIDS,
    )
    datapoints = cursor.fetchall()

    for dp_id, ecu_address, did, name in datapoints:
        ecu_hex = format(int(ecu_address), "03x")
        fields = MIXER_FIELDS if did in MIXER_ROOM_SENSOR_DIDS else ROOM_FIELDS
        for sub_field, device_class, unit in fields:
            unique_id = "o3e_{}_{}_{}".format(
                ecu_hex, did, sub_field.lower()
            )
            entity_name = "{} {}".format(humanize(name), humanize(sub_field))
            cursor.execute(
                """
                INSERT INTO ha_entities
                    (dp_id, entity_type, unique_id, name, device_class, unit,
                     enabled, sub_field)
                VALUES (?, 'sensor', ?, ?, ?, ?, 1, ?)
                ON CONFLICT(unique_id) DO NOTHING
                """,
                (dp_id, unique_id, entity_name, device_class, unit, sub_field),
            )


def apply_hacs_datapoint_preset(cursor):
    if not table_exists(cursor, "datapoints"):
        return

    placeholders = ",".join("?" for _ in HACS_BASE_DIDS)
    cursor.execute(
        """
        UPDATE datapoints
        SET poll_enabled = 1,
            poll_priority = 1
        WHERE did IN ({})
          AND poll_enabled = 0
          AND poll_priority = 0
        """.format(placeholders),
        HACS_BASE_DIDS,
    )


db_path = os.environ.get("OPEN3E_DB_PATH", "/data/open3e_web.db")
conn = sqlite3.connect(db_path)
try:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    set_setting(cursor, "web_port", os.environ.get("OPEN3E_WEB_PORT", "5051"))
    set_setting(cursor, "can_interface", os.environ.get("OPEN3E_CAN_INTERFACE"))
    set_setting(cursor, "can_bitrate", os.environ.get("OPEN3E_CAN_BITRATE", "250000"))
    set_setting(cursor, "mqtt_host", os.environ.get("OPEN3E_MQTT_HOST"))
    set_setting(cursor, "mqtt_port", os.environ.get("OPEN3E_MQTT_PORT", "1883"))
    set_setting(cursor, "mqtt_user", os.environ.get("OPEN3E_MQTT_USER"))
    set_setting(cursor, "mqtt_password", os.environ.get("OPEN3E_MQTT_PASSWORD"))
    set_setting(cursor, "mqtt_topic_prefix", os.environ.get("OPEN3E_MQTT_TOPIC_PREFIX"))
    mqtt_format = os.environ.get("OPEN3E_MQTT_FORMAT_STRING") or DEFAULT_MQTT_FORMAT
    if mqtt_format == LEGACY_ADDON_MQTT_FORMAT:
        mqtt_format = DEFAULT_MQTT_FORMAT
    set_setting(cursor, "mqtt_format_string", mqtt_format)
    set_setting(cursor, "mqtt_client_id", os.environ.get("OPEN3E_MQTT_CLIENT_ID"))
    set_setting(
        cursor,
        "mqtt_publish_json",
        bool_setting(os.environ.get("OPEN3E_MQTT_PUBLISH_JSON"), default=False),
    )

    if bool_setting(os.environ.get("OPEN3E_AUTO_SELECT_HACS_DATAPOINTS"), default=True) == "1":
        apply_hacs_datapoint_preset(cursor)

    if bool_setting(os.environ.get("OPEN3E_AUTO_SELECT_ROOM_DATAPOINTS"), default=True) == "1":
        apply_room_datapoint_preset(cursor)

    conn.commit()
finally:
    conn.close()
