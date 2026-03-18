import argparse
import logging
import yaml
import numpy as np
import pandas as pd
import time
import json



def setSeed(seed):
    np.random.seed(seed)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    return parser.parse_args()



def setuplogging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )


def loadConfig(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    required = ["seed", "window", "version"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    return config


def loadData(path):
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty")

    df.columns = df.columns.str.strip()

    if "close" not in df.columns:
        raise ValueError(f"Missing required column: close. Found columns: {list(df.columns)}")

    return df


def computeRolling(df, window):
    df["rolling_mean"] = df["close"].rolling(window).mean()
    return df

def generateSignal(df):
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    return df




def computeMetrics(df, start_time, config):
    latency_ms = int((time.time() - start_time) * 1000)

    return {
        "version": config["version"],
        "rows_processed": len(df),
        "metric": "signal_rate",
        "value": round(float(df["signal"].mean()),4),
        "latency_ms": latency_ms,
        "seed": config["seed"],
        "status": "success"
    }



def write_metrics(output_path, data):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)




def main():
    args = parse_args()
    setuplogging(args.log_file)

    import time
    start_time = time.time()

    try:
        logging.info("Job started")

        config = loadConfig(args.config)
        logging.info(f"Config loaded: {config}")

        setSeed(config["seed"])

        df = loadData(args.input)
        logging.info(f"Loaded {len(df)} rows")

        df = computeRolling(df, config["window"])
        logging.info("Rolling mean computed")

        df = generateSignal(df)
        logging.info("Signals generated")

        metrics = computeMetrics(df, start_time, config)
        write_metrics(args.output, metrics)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics)) 

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, error_output)
        logging.error(str(e))

        print(json.dumps(error_output))
        exit(1)


if __name__ == "__main__":
    main()