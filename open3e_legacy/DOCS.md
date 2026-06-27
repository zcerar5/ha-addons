# Open3e Legacy Add-on Documentation

This add-on is the classic Open3e MQTT listener for the Open3e HACS integration. It is based on the `0.6.5` add-on behavior and does not include the Open3e Web UI.

## Requirements

- Home Assistant OS or Home Assistant Supervised.
- Mosquitto broker installed and configured in Home Assistant.
- A CAN adapter connected to the Home Assistant host.

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `can` | `can0` | CAN interface used to communicate with the E3 device. |
| `Listen_Topic` | `open3e/cmnd` | MQTT topic where Open3e listens for commands. |
| `Server_Topic` | `open3e` | MQTT topic where Open3e publishes data. |
| `MQTT_FormatString` | `{device}_{ecuAddr:03X}_{didNumber}_{didName}` | Format used to build MQTT entity topic names. |
| `MQTT_ClientID` | `open3e` | MQTT client ID used by Open3e. |

The first start may take longer because `open3e_depictSystem` creates `/data/devices.json`.

Use this add-on when Open3e HACS should control polling through `open3e/cmnd`. Stop the WebUI add-on before starting this legacy add-on so both add-ons do not compete for the same CAN interface.

## Terminal

The add-on exposes a terminal through Home Assistant ingress. Start the add-on and use **Open Web UI** to open a shell inside the Open3e Legacy add-on container.

The terminal is intended for Open3e troubleshooting commands such as `open3e --help`, `open3e_depictSystem --help`, and inspecting files in `/data`. It is not a host shell.

## Finding which DID a hardware control writes

A physical room control such as a **Vitotrol 300-E** talks to the heat pump over the same E3 CAN bus that Open3e uses. When you change a temperature on it, it writes a value to a datapoint (DID) on the bus. The `open3e_capture` helper finds that DID so it can later be exposed in Home Assistant as a writable entity.

In this add-on the legacy `open3e --listen` listener holds the CAN bus, so first **pause the Open3e HACS integration polling** to keep the bus quiet, then in the ingress terminal run:

1. `open3e_capture snapshot before`
2. Change the temperature on the Vitotrol, then wait ~30 seconds.
3. `open3e_capture snapshot after`
4. `open3e_capture diff before after`

The diff lists every datapoint that changed, temperature-like entries first; the one matching the value you dialled in is the write target. By default a snapshot reads only temperature/setpoint-like datapoints; add `--all` to both snapshots if the diff shows nothing. Snapshots are saved under `/data/open3e_captures/`.

This fork installs Open3e from upstream `develop` for the classic MQTT add-on and exposes ViCare/ZigBee room device current values in the Vitocal/Vcal and Vitodens/Vdens profiles. That lets the Open3e HACS integration create room temperature and humidity entities when those datapoints are present on the bus.

## Support

Open3e upstream discussion: https://github.com/open3e/open3e/discussions/216
