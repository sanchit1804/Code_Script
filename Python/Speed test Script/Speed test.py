import speedtest
import argparse
import csv
import json
from datetime import datetime
import sys

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Convert to Mbps
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "download_mbps": round(download, 2),
        "upload_mbps": round(upload, 2),
        "ping_ms": round(ping, 2),
    }

def save_csv(data, filename="results.csv"):
    header = ["timestamp", "download_mbps", "upload_mbps", "ping_ms"]
    try:
        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
        print(f"✅ Results saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")

def save_json(data, filename="results.json"):
    try:
        with open(filename, "a") as f:
            json.dump(data, f)
            f.write("\n")
        print(f"✅ Results saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Internet Speed Test & Logger")
    parser.add_argument("--save", choices=["csv", "json"], help="Save results to CSV or JSON")

    # ✅ Ignore unwanted Colab/Jupyter args like -f kernel.json
    args, unknown = parser.parse_known_args(sys.argv[1:])

    print("🚀 Running speed test... please wait.\n")
    results = test_speed()

    print(f"Download Speed: {results['download_mbps']} Mbps")
    print(f"Upload Speed:   {results['upload_mbps']} Mbps")
    print(f"Ping:           {results['ping_ms']} ms")

    if args.save == "csv":
        save_csv(results)
    elif args.save == "json":
        save_json(results)
