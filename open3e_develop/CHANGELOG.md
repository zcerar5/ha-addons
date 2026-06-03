# Changelog

## 0.6.7-dev

- Add an option to auto-select the base datapoints used by the Open3e HACS integration.
- Keep the room datapoint preset for develop room-current temperature and humidity values.

## 0.6.6-dev

- Match the default MQTT format to the Web UI Home Assistant discovery topics.
- Default MQTT publishing to split subtopics for Home Assistant subfield sensors.
- Add an option to auto-select discovered room temperature and humidity datapoints at low priority.

## 0.6.5-dev

- Start the Open3e Web UI instead of the legacy CLI listener.
- Expose the Web UI on port `5051`.
- Install Open3e with its `web` dependencies.

## 0.6.4-dev

- Added as a separate add-on variant that builds Open3e from the upstream `develop` branch.
- Uses separate default MQTT topics and client ID from the stable Open3e add-on.

## 0.6.3

- Added current Home Assistant repository metadata.
- Updated the fork to publish images as `ghcr.io/zcerar5/ha-addon-open3e`.
- Replaced example translations with Open3e configuration translations.
- Added add-on documentation.

## 0.6.2

- Upstream release from `flecke-m/ha-addons`.
