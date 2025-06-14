import csv
import os
from datetime import datetime

def log_interaction(query, reply, status, log_path="complaint_log.csv"):
    file_exists = os.path.isfile(log_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Query", "Response", "Status"])
        writer.writerow([timestamp, query, reply, status])


def load_env_variables(path=".env"):
    env_vars = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    env_vars[key.strip()] = val.strip()
    return env_vars
