# Changelog

## 0.6.10

- Decode the Vitotrol room remote (ViCare device type 8) on the ZigBee bus: temperature and humidity are now published like other room devices. Layout confirmed against a live Vitotrol 300-E capture.
- Name device type 8 in the ViCareDeviceTypes enum.

## 0.6.9

- Flatten the new O3ESwitch ZigBee payloads before MQTT publishing: `ActualTemperature`, `Humidity` and other device fields are published at the top level again, with `ViCareDevice` as a plain `{ID, Text}` enum.
- Restores compatibility with the Open3e HA integration and MQTT discovery consumers that parse the pre-0.6.8 payload shape, while keeping the corrected temperature decoding.

## 0.6.8

- Update Open3e to current upstream `develop` (pinned commit) with the new `O3ESwitch` ZigBee room device codec.
- Fixes room sensors whose temperature decoded as ~0.3 °C: values are now decoded per device type (climate sensor, TRV, floor thermostat, actuator).
- Re-run system depiction once after update so the new codecs are used for discovered ECUs. The first start after updating takes longer.

## 0.6.7

- Add the `open3e_capture` helper to find which DID a hardware control (e.g. a Vitotrol 300-E room remote) writes when you change a setting.
- The helper enumerates DIDs from `devices.json` so it works without the Web UI database; run it from the ingress terminal.

## 0.6.6

- Add a Home Assistant ingress terminal for the legacy add-on.
- Keep the classic Open3e HACS MQTT listener behavior unchanged.

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
