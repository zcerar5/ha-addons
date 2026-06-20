# Heat pump short cycling alerts & protection

Two-tier handling of heat pump short cycling (the refrigeration circuit
switching mode too frequently, which wastes energy and wears the compressor).

| Tier | What it does | File |
|------|--------------|------|
| **Alert** | Notify on each short cycle (mode held < 10 min) | `heatpump_short_cycle_alert.yaml` |
| **Protect** | After **5 short cycles within 60 min**, turn OFF space heating/cooling, **keep DHW on** | `heatpump_short_cycle_protect.yaml` |
| Reset | Resets the rolling counter when short cycling stops | `heatpump_short_cycle_reset.yaml` |
| Helpers | Counter + timer the above rely on | `helpers.yaml` |

## How it works

1. `heatpump_short_cycle_alert.yaml` triggers on every mode change of
   `sensor.vitocal_7470570540430221_refrigeration_circuit_mode` and measures how
   long the **previous** mode was held. If it was shorter than `min_cycle_minutes`
   (default **10**), it notifies, increments `counter.heatpump_short_cycles`, and
   (re)starts the 60-minute `timer.heatpump_short_cycle_window`.
2. `heatpump_short_cycle_reset.yaml` resets the counter to 0 when that timer
   elapses (i.e. 60 min with no further short cycle) — giving a rolling
   "5 within 60 minutes" window.
3. `heatpump_short_cycle_protect.yaml` triggers when the counter reaches **5**
   and turns off the heating/cooling `climate` entities, then resets the counter.
   **DHW is untouched** because hot water is a separate `water_heater` entity.

## Thresholds (suggested)

- `min_cycle_minutes: 10` — what counts as a "short" cycle (tune 6–15).
- Upper limit: **5 short cycles / 60 min** before auto-disabling heating/cooling.
  Change it by editing `above:` in `heatpump_short_cycle_protect.yaml`
  (`above: N-1`) and the timer `duration` in `helpers.yaml`.

## Getting this into Home Assistant

These files are **not** auto-applied — Home Assistant doesn't read automations
from this add-on repo. Copy them into your HA config one of two ways:

- **UI:** create the helpers under Settings → Helpers, then paste each
  `heatpump_short_cycle_*.yaml` into Settings → Automations → *Edit in YAML*.
- **File editor / Samba / Studio Code Server:** append
  `automations.yaml.append` to your `automations.yaml`, add `helpers.yaml` to
  `configuration.yaml`, then restart / reload automations.

## Install

1. **Helpers:** add `helpers.yaml` contents to your `configuration.yaml`
   (or a package) and restart HA, or recreate the `counter` and `timer` via
   **Settings → Devices & services → Helpers**.
2. **Automations:** for each `*.yaml` automation, go to
   **Settings → Automations & scenes → Create automation → Edit in YAML** and
   paste the contents.
3. **⚠️ Verify entity IDs** in `heatpump_short_cycle_protect.yaml`. It currently
   turns off **both** candidate heating entities:
   - `climate.vitocal_climate_circuit_1` ("Vitocal Climate circuit 1")
   - `climate.e3_vitocal_16_heating` ("E3 Vitocal 16 Heating")

   Confirm the real entity IDs in **Developer Tools → States** and remove the one
   that doesn't apply.
4. Update the notification `device_id` if you want a different target.

## Notes

- Re-enabling heating/cooling after a protection trip is **manual** (turn the
  climate entity back on once the cause is resolved).
- The protection fires once per episode (it resets the counter), so you won't be
  spammed; you still get the per-cycle alerts up to the limit.
