# Heat pump short cycling alert

`heatpump_short_cycle_alert.yaml` notifies you when the heat pump's
refrigeration circuit changes mode **too soon** after the previous change — a
sign of short cycling (the compressor switching on/off too frequently, which
wastes energy and wears the unit).

## How it works

- Triggers on any state change of
  `sensor.vitocal_7470570540430221_refrigeration_circuit_mode`
  (ignoring `unknown`/`unavailable`, e.g. on restart).
- Measures how long the circuit stayed in the **previous** mode.
- Only notifies when that duration is **less than `min_cycle_minutes`**.

## Suggested threshold

`min_cycle_minutes: 10`

A healthy heat pump should hold a mode for several minutes; a minimum cycle
time of ~10 minutes is a common rule of thumb (more than ~3–4 starts per hour
is a warning sign). Tune between **6 and 15 minutes** to match your unit and
how sensitive you want the alert to be.

## Install

1. **Settings → Automations & scenes → Create automation → Edit in YAML**, then
   paste the contents of `heatpump_short_cycle_alert.yaml`.
2. Adjust `min_cycle_minutes` if needed.
3. The notification target `device_id` is carried over from the original
   automation — update it if you want to notify a different device/service.
