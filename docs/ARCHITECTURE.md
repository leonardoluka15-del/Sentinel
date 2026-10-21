# Architecture

The standard-library entry point creates one `Engine`, one background `Worker`, and a `ThreadingHTTPServer`. A reentrant engine lock serializes scenario mutations, sampling, acknowledgement, and snapshot assembly. Each SQLite operation uses its own connection with WAL enabled and parameterized queries. HTTP requests and sampling use the same engine instance.

## Data flow

1. `inventory.py` and `links.py` construct the model.
2. `simulator.py` generates bounded synthetic measurements. Hub outage propagation follows the cluster model.
3. `repository.py` writes telemetry. `detection.py` evaluates thresholds and robust CPU signals.
4. `incidents.py` reconciles active findings with open or acknowledged incidents. Missing findings resolve automatically.
5. `engine.py` assembles telemetry, forecasts, statistical plugins, topology impact, correlations, SLA sampling and audit events.
6. The browser fetches a snapshot every five seconds and renders all surfaces without external libraries or CDNs.

## Invariants

- At most one active incident exists per device and signal through serialized reconciliation.
- Acknowledgement does not suppress measurement collection or fault recovery.
- Device identifiers must belong to the inventory.
- Scenario changes and snapshot assembly cannot interleave with each other.
- Predictions and correlation hypotheses are labeled with their limitations.

## Extension contracts

For a real telemetry adapter, produce records with `ts`, `device`, `cpu`, `latency`, `loss`, `traffic`, and `available`. Validate units, timestamps, bounds, inventory membership, and authorization before replacing the simulator sampling call. The existing code does not provide this adapter.

An analytics plugin is a checked-in module under `sentinel/analytics/` with `calculate(xs)` returning a finite numeric result for empty, constant, short, and typical finite inputs. Registry discovery skips private modules and itself. Runtime upload of Python is intentionally unsupported.

Future device imports should use a data-only schema and parameterized persistence. Production identity, distributed scheduling, database migrations, and deployment observability require additional implementation.
