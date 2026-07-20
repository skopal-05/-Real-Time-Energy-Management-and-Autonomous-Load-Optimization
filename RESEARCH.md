# Week 2 Research Notes - Persons 1 and 2

## Person 1

### Industrial digital twin concepts

An industrial digital twin is a continuously updated software representation of a physical asset. The implementation separates four concerns: state validation records what the asset is doing, synchronization carries telemetry into the twin, behaviour learning estimates relationships between signals, and simulation evaluates a proposed state without changing the live state. Keeping those concerns separate makes sensor faults easier to isolate and scenario results easier to audit.

### Production-line behaviour modelling

Production throughput depends on machine load, motor temperature, and vibration. The production twins learn the relationship between those inputs and units per hour as telemetry arrives. Their scenario outputs also expose specific energy use (`kWh/unit`), which helps compare throughput changes with their energy cost. Temperature and vibration are range-checked before a state can enter the twin so unrealistic sensor values cannot train the behaviour model.

### Boiler state synchronization

The boiler twin synchronizes steam pressure and flow, fuel flow, feedwater temperature, flue-gas temperature, and measured efficiency as one timestamped state. Simulation estimates efficiency, steam-to-fuel ratio, and thermal loss. Atomic state updates are important because combining readings from different timestamps could produce a physically misleading efficiency estimate.

## Person 2

### Renewable-energy digital twin

The solar twin relates irradiance, panel temperature, and DC power to inverter output. Its scenarios report inverter power, conversion efficiency, and energy for a 15-minute interval. Anchoring learned changes to the latest synchronized measurement lets the model respond to irradiance scenarios while remaining consistent with the physical inverter's current operating point.

### Battery state modelling

Battery state is represented by state of charge, signed power, voltage, current, temperature, and operating mode. The Week 1 convention uses positive power for charging and negative power for discharging. The simulation applies an energy balance to a documented 500 kWh nominal capacity and clamps state of charge to the physical 0-100% range.

### Grid synchronization

The grid twin synchronizes imports, exports, frequency, voltage, power factor, and tariff. It models net power as import minus export, calculates 15-minute import cost, and flags frequency stability against a 49.5-50.5 Hz operating band. The state validator uses wider acceptance limits so abnormal-but-possible observations can be retained and surfaced rather than silently discarded.

## Implementation decision

The behaviour learner is intentionally dependency-free and updates online with each observation. Scenario predictions are anchored to the latest measured target, then adjusted by the learned response to changed inputs. This design is lightweight enough for the Week 2 prototype and keeps later replacement with a trained forecasting model straightforward.

