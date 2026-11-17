# Changelog

## 0.6.13

- Update Open3e from the August `develop` pin (0.7.7) to upstream `develop` of 22 Oct 2026 (0.7.10, commit `756237b`). The three patches (room DIDs, ZigBee payload flattening, Vitotrol decode) apply unchanged.
- ZigBee room current values (DIDs 2086-2143 and 2262-2319): the first byte is now decoded as `ConnectionState` (`{ID, Text}`: 3 Connected, 5 Not reachable, 0 Empty slot) instead of the raw `Unknown_00` field. All other fields, including the flattened `ActualTemperature` and `Humidity`, are unchanged.
- ZigBee device properties: `Hardware-Version` is decoded instead of the raw `Unknown2` field.
- Writes to a single field of a DID now check the encoded length, and a failed write no longer leaves Open3e publishing raw values as bytes until restart.
- DID 2428 renamed to `MixerThreeCircuitRoomEcoFunctionSettings` (typo fix), which changes its MQTT topic.
- Not included yet on purpose: the corrected `OpStates`/`Errors` enums of Open3e 0.7.11 and later. Open3e encodes enum fields by their text, and the HACS climate HVAC-mode write sends `State` as `No request`, which 0.7.11 moves from 12 to 255. The write would then send `0xFF` instead of today's `0x0C` in the `State` byte of DIDs 1415-1418, which is not yet verified on a Vitocal 222-S. This pin keeps that write byte-identical.
- The system depiction runs once on the first start after this update (new marker `/data/.open3e-room-dids-0.6.13`), so the first start takes a few minutes.

## 0.6.12

- Revert the 0.6.11 behavior of re-running the (long) system depiction on every add-on update.
- Depiction now runs only when needed: force it manually by removing the marker file (`rm /data/.open3e-room-dids-*` in the terminal) and restarting the add-on. Releases that require re-depiction for everyone will bump the marker name explicitly.

## 0.6.11

- Re-run system depiction on every add-on update: the generated depiction files in `/data` embed codec definitions, so codec patches (like the Vitotrol decode in 0.6.10) only take effect after regeneration. The first start after each update takes a few minutes.

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
