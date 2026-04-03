
import csv, os, datetime, uuid

def trace_id():
    return str(uuid.uuid4())

def log(trace_id, stage, data):
    try:
        os.makedirs("output", exist_ok=True)

        file_path = os.path.join("output", "processing_log.csv")
        file_exists = os.path.isfile(file_path)

        timestamp = datetime.datetime.utcnow().isoformat()

        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["time", "trace_id", "stage", "data"])

            writer.writerow([timestamp, trace_id, stage, str(data)])

        # Console debug (optional)
        print(f"[TRACE {trace_id}] {stage} → {data}")

    except PermissionError:
        print("❌ File is locked or permission denied (close Excel!)")
    except Exception as e:
        print(f"❌ Logging failed: {e}")