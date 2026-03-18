#  MLOps Batch Signal Pipeline

##  Overview

This project implements a **minimal MLOps-style batch job** that processes OHLCV market data to generate trading signals.

The pipeline demonstrates core **MLOps engineering practices**:

* Reproducibility using configuration + seed
* Observability using structured logs and metrics
* Deployment readiness using Docker

The program reads a dataset, computes a rolling mean on the `close` price, generates a binary signal, and outputs structured metrics.

---

#  Pipeline Workflow

1. Load configuration from `config.yaml`
2. Validate input dataset (`data.csv`)
3. Compute rolling mean of the `close` column
4. Generate binary trading signal
5. Produce machine-readable metrics
6. Log execution details

Signal logic:

```
signal = 1 if close > rolling_mean
signal = 0 otherwise
```

---

#  Project Structure

```
mlops-task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

---

#  Run Locally (Python)

## Create Virtual Environment (Recommended)

```
python -m venv venv
```

Activate the environment:

### Linux / macOS

```
source venv/bin/activate
```

### Windows

```
venv\Scripts\activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Run the Pipeline

```
python run.py \
--input data.csv \
--config config.yaml \
--output metrics.json \
--log-file run.log
```

---

# Run Using Docker

Docker allows the pipeline to run **without installing Python or dependencies locally**.

## Build Docker Image

```
docker build -t mlops-task .
```

## Run Container

```
docker run --rm mlops-task
```

The container will automatically:

* execute the pipeline
* generate `metrics.json`
* generate `run.log`
* print the metrics to stdout

---

# Example Output

Example `metrics.json`:

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4989,
  "latency_ms": 29,
  "seed": 42,
  "status": "success"
}
```

---

# Logging

Detailed logs are written to `run.log`.

Logs include:

* Job start timestamp
* Config validation
* Dataset loading
* Rolling mean computation
* Signal generation
* Metrics summary
* Job completion status

---

# Error Handling

If an error occurs, the pipeline still writes a metrics file:

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of failure"
}
```

This ensures machine-readable output even on failure.

---

# Reproducibility

Reproducibility is ensured using configuration parameters.

Example `config.yaml`:

```
seed: 42
window: 5
version: "v1"
```

The seed guarantees deterministic runs.

---

# Requirements

* Python 3.9+
* Docker (optional, for containerized execution)

---

# Author

**Vikram Jaiswal**
