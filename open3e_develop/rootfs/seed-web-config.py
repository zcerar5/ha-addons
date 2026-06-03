#!/usr/bin/env python3
"""Seed Open3e Web UI settings from Home Assistant add-on options."""

import os
import sqlite3

DEFAULT_MQTT_FORMAT = "{didNumber}_{didName}"
LEGACY_ADDON_MQTT_FORMAT = "{device}_{ecuAddr:03X}_{didNumber}_{didName}"
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

    if bool_setting(os.environ.get("OPEN3E_AUTO_SELECT_ROOM_DATAPOINTS"), default=True) == "1":
        apply_room_datapoint_preset(cursor)

    conn.commit()
finally:
    conn.close()
