# Open3e Add-on Documentation

This add-on installs Open3e from the upstream `develop` branch. By default it starts the Open3e Web UI on port `5051` and lets the Web UI control CAN polling and MQTT publishing.

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Web_UI_Enabled` | `true` | Start the Open3e Web UI. |
| `Controller_Mode` | `webui` | `webui` lets Open3e Web UI control CAN polling and MQTT publishing. `open3e-ha` starts the legacy MQTT command listener for the Open3e HACS integration and keeps Web UI passive. |
| `Web_UI_Port` | `5051` | Port used by the Open3e Web UI. |
| `Listen_Topic` | `open3e/cmnd` | MQTT topic where the legacy Open3e listener receives commands from the Open3e HACS integration. |
| `Server_Topic` | `open3e` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{device}_{ecuAddr:03X}_{didNumber}_{didName}` | Format used to build MQTT entity topic names. This default matches the original add-on and Open3e HACS integration flow. |
| `MQTT_ClientID` | `open3e` | MQTT client ID used by Open3e. |
| `MQTT_Publish_JSON` | `false` | Web UI mode setting. Keep disabled for Home Assistant so complex datapoints are published as split subtopics. |
| `Auto_Select_HACS_Datapoints` | `false` | Web UI mode setting. Preselect the base datapoints used by the Open3e HACS integration. Disabled by default so Open3e HACS remains the polling controller. |
| `Auto_Select_Room_Datapoints` | `false` | Web UI mode setting. Preselect discovered room temperature and humidity datapoints. Disabled by default so Open3e HACS remains the polling controller. |

## Controller modes

`webui` is the default mode. The Open3e Web UI owns CAN access, polling selection, MQTT publishing, and optional Home Assistant discovery.

`open3e-ha` is the compatibility mode for the Open3e HACS integration. The add-on starts the legacy `open3e --listen open3e/cmnd` MQTT listener, so Open3e HACS requests system information and feature values through `open3e/cmnd`, as with the original add-on. In this mode the Web UI still opens on port `5051`, but the add-on clears Web UI CAN and MQTT settings so it does not become a second polling controller.

Open the Web UI from the add-on page or at `http://<home-assistant-host>:5051`.

If `devices.json` and generated `Open3Edatapoints_*.py` files already exist in `/data`, the add-on imports them into the Web UI database during startup. That keeps discovered ECUs and datapoints visible after switching between controller modes.

The Web UI Write Values page is available for writable datapoints discovered on your system. Writing through that page requires `Controller_Mode` to be `webui`, because `open3e-ha` mode keeps the Web UI CAN engine passive.

## Web UI Terminal

The Web UI includes a restricted Terminal page for Open3e CLI tools. It runs commands from `/data` inside the add-on container and allows only `open3e`, `open3e_depictSystem`, `open3e_dids2json`, `open3e_dids2md`, and `open3e_topology`.

It does not expose a general-purpose Linux shell. Shell features such as pipes, redirects, command chaining, and arbitrary commands are intentionally unavailable.

This fork exposes ViCare/ZigBee room device current values in the Vitocal/Vcal and Vitodens/Vdens profiles. That lets Home Assistant create room temperature and humidity entities when those datapoints are present on the bus.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
