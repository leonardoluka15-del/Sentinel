# ◈ SENTINEL
### Network intelligence, from signal to response.

A runnable Python network operations simulator with a dark browser dashboard, interactive topology, statistical analysis, capacity forecasts, persistent incidents, and controlled failure injection.

**61 Python files · 30 analytics plugins · 48 simulated nodes · 6 regions · No third-party runtime dependencies**

Built for Leonard Oluka. All telemetry is synthetic; this repository contains no company or customer network data.

## Run

Requires Python 3.10 or later. No pip install, API keys, GPU, or paid services.

```bash
python app.py
```

Open **http://localhost:8501** in your browser. Keep the Python process running. On Windows, `py app.py` also works when the Python launcher is installed.

This is a Python web application, **not a Streamlit application**. Use `python app.py`, not `streamlit run app.py`. The repository alone does not create a hosted website.

## Try a complete investigation

1. Open **Simulation studio** and select `SNT-001` in the device selector.
2. Choose **Node outage**. This hub failure interrupts eight nodes in the Lagos access cluster.
3. Open **Incident desk** to inspect the availability incidents and regional correlation hypothesis.
4. Acknowledge an open incident. It remains acknowledged until the fault clears.
5. Explore **Network topology** to inspect the node removal impact.
6. Return to Simulation studio and choose **Restore normal operation**. Availability incidents automatically resolve on the next sample.
7. Open **Activity & exports** to download the investigation snapshot or selected telemetry.

## Application surfaces

| Surface | Implemented behavior |
|---|---|
| Command centre | Current availability, active incidents, aggregate simulated traffic, latency, regional health, trends |
| Network topology | Clickable SVG topology, structural node removal analysis, ranked impact |
| Intelligence lab | 30 CPU statistics, traffic history, six-sample linear capacity outlook |
| Incident desk | Threshold/statistical alerts, deduplication, acknowledgement, automatic recovery, regional hypotheses |
| Simulation studio | Congestion, node outage, packet loss, CPU overload, restoration, manual sample advance |
| Activity & exports | Persisted audit events, UTF-8 CSV telemetry and JSON evidence snapshot |

## How it works

`app.py` → CLI → simulation worker + threaded HTTP server → engine → repositories, graph analysis, analytics plugins → SQLite → browser dashboard.

- Seeded pseudorandom simulator bootstraps 72 historical ticks, then samples every five seconds.
- A ring backbone joins six access clusters: Lagos, Abuja, Port Harcourt, Nantes, Paris, and Lyon.
- CPU >90%, latency >80 ms, loss >2%, capacity >85%, unavailability, and selected robust z-score signals create incidents.
- Scenario changes apply immediately. Only one injected scenario is active at a time.
- Fault state resets to normal on restart; stored samples, incident history, and audit events persist.
- Up to 92,160 recent telemetry rows are retained (approximately 160 minutes at the default cadence). The UI shows the latest 120 samples per device. Incident and audit histories are also bounded.
- All 30 analytics modules are discovered from the local analytics package and run by the engine. No uploaded executable plugins are accepted.

## Configuration

```bash
python app.py --port 8502 --interval 10 --database data/custom.db
```

For access from another machine, provide an access token of at least 16 characters and bind explicitly:

```bash
# Linux / macOS
export SENTINEL_TOKEN='replace-with-a-long-random-secret'
python app.py --host 0.0.0.0
```

```powershell
# Windows PowerShell
$env:SENTINEL_TOKEN='replace-with-a-long-random-secret'
python app.py --host 0.0.0.0
```

Use **Access** in the dashboard to enter the token. It stays in the browser tab's session storage. `PORT` can supply the default server port. A blank token is permitted only for local binding.

Remote deployment requires a TLS reverse proxy and appropriate network access controls. The standard-library HTTP server is intended for demonstration and development. The token grants one shared operator role; there are no per-user accounts or RBAC.

## Docker

```bash
docker build -t sentinel .
docker run --rm -p 8501:8501 -e SENTINEL_TOKEN='replace-with-a-long-random-secret' -v sentinel-data:/app/data sentinel
```

The container runs as an unprivileged user. Mount `/app/data` for persistence. No hosting provider or deployment has been provisioned by this repository.

## API

All `/api/*` routes require `Authorization: Bearer <SENTINEL_TOKEN>` when a token is configured. Static assets and `/health` are public.

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Liveness and simulation mode |
| GET | `/api/state?device=SNT-001` | Consistent investigation snapshot |
| GET | `/api/scenarios` | Available failure scenarios |
| GET | `/api/export.csv?device=SNT-001` | Selected history |
| GET | `/api/report.json?device=SNT-001` | Investigation JSON |
| POST | `/api/scenario` | `{"scenario":"outage","target":"SNT-001"}` |
| POST | `/api/acknowledge` | `{"id":1}` |
| POST | `/api/step` | `{}` advances the simulator |

Cross-origin browser writes are rejected. Request bodies are bounded; database queries use parameters. Exceptions are logged server-side without exposing tracebacks in API responses.

## Validation

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py sentinel tests
```

The seven integration/unit tests exercise analytics, fault scenarios, graph paths, persistence, incident lifecycle, HTTP endpoints, authentication, and rejected cross-origin writes. GitHub Actions runs these on Python 3.10–3.13.

## Scope and limitations

This first version is a working simulation and engineering portfolio application, not a production NMS. It does not collect SNMP/NETCONF/Prometheus telemetry, send external alerts, execute remediation, or include a trained AI model. Regional correlation is a heuristic hypothesis, not proven root cause. Forecast intervals are heuristic and not calibrated probabilities. Topology analysis models node removal, not routing convergence. Availability is based on retained sampled observations, not a contractual monthly SLA. Different chart lines can have different units, as labeled.

The initial ambition is delivered through working modules rather than artificially inflated source volume. This project does **not** contain five million lines of code.

## Structure

```text
app.py                    Entry point
sentinel/core/            Simulation, SQLite, incidents, topology, forecasting, CLI
sentinel/analytics/       Thirty statistical plugins and registry
sentinel/web/             HTTP API, security, responses, browser assets
tests/                    Seven behavioral tests
docs/                     Architecture and extension notes
.github/workflows/        Continuous integration
```

## Next engineering milestones

- Read-only telemetry adapters with schema validation and credential isolation.
- Timestamp-aware forecasting with chronological backtesting and calibrated uncertainty.
- Multi-user identity, permissions, and production application server.
- Time-indexed incident replay and configurable policy rules.
- Integration with a user-selected hosting environment.

MIT License.
