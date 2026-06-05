# Changelog

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
