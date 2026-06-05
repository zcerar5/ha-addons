# Changelog

## 0.6.14

- Fix the Web UI Write Values page when upstream `Open3Edatapoints_writables.json` is not present.
- Use the Web UI Home Assistant writable entity definitions as the writable DID fallback.

## 0.6.13

- Import existing `devices.json` and generated datapoint files into the Web UI database during add-on startup.
- Keep depiction results visible in Web UI when switching between `webui` and `open3e-ha` controller modes.

## 0.6.12

- Add a restricted Open3e Terminal page to the Web UI.
- Allow running Open3e CLI tools from the add-on container without exposing a general-purpose shell.

## 0.6.11

- Add `Controller_Mode` with `webui` as the default and `open3e-ha` as the compatibility mode.
- In `webui` mode, let the Open3e Web UI own CAN polling and MQTT publishing.
- In `open3e-ha` mode, start the legacy MQTT command listener and keep the Web UI passive so both controllers do not compete.

## 0.6.10

- Enable the Open3e Web UI by default while still running the legacy MQTT listener for Open3e HACS compatibility.
- Keep Web UI datapoint auto-selection disabled by default so Open3e HACS remains the default polling controller.

## 0.6.9

- Default back to the legacy Open3e MQTT listener so the Open3e HACS integration controls which datapoints are requested.
- Add `Web_UI_Enabled` to switch explicitly into Open3e Web UI mode.
- Restore the legacy default MQTT format string for HACS compatibility.

## 0.6.8

- Build the add-on locally from the Dockerfile instead of pulling a prebuilt GHCR image.

## 0.6.7

- Start the Open3e Web UI on port `5051` from the main `open3e` add-on.
- Install Open3e with its `web` dependencies from upstream `develop`.
- Seed Web UI CAN, MQTT, HACS datapoint, and room datapoint settings from Home Assistant add-on options.

## 0.6.6

- Keep Open3e discovery generation unchanged; uninstalling and reinstalling the add-on can regenerate `/data/devices.json` when needed.

## 0.6.5

- Advertise ViCare/ZigBee room device current values for Vitocal/Vcal as well as Vitodens/Vdens profiles.
- Refresh the generated Open3e device description once so existing add-on installs can expose newly supported room datapoints.

## 0.6.4

- Install Open3e from the upstream `develop` branch for the classic MQTT add-on.
- Advertise ViCare/ZigBee room device current values for the Vdens profile so the Open3e HACS integration can create room temperature and humidity entities.

## 0.6.3

- Added current Home Assistant repository metadata.
- Updated the fork to publish images as `ghcr.io/zcerar5/ha-addon-open3e`.
- Replaced example translations with Open3e configuration translations.
- Added add-on documentation.

## 0.6.2

- Upstream release from `flecke-m/ha-addons`.
