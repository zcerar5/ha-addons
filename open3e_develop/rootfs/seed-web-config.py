#!/usr/bin/env python3
"""Seed Open3e Web UI settings from Home Assistant add-on options."""

import os
import sqlite3


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
    set_setting(cursor, "mqtt_format_string", os.environ.get("OPEN3E_MQTT_FORMAT_STRING"))
    set_setting(cursor, "mqtt_client_id", os.environ.get("OPEN3E_MQTT_CLIENT_ID"))

    conn.commit()
finally:
    conn.close()
