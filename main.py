import subprocess
import csv
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_FILE = "metrics_log.csv"
INTERVAL = 0.5  # másodperc

def get_metrics():
    """
    Lefuttatja a powermetrics parancsot és kinyeri a CPU és GPU fogyasztási adatokat.
    """
    try:
        result = subprocess.run(
            ["sudo", "powermetrics", "--samplers", "cpu_power,gpu_power", "--show-usage-summary", "-n1"],
            capture_output=True,
            text=True
        )
        output = result.stdout

        cpu_power = None
        gpu_power = None

        for line in output.splitlines():
            if "CPU Power" in line:
                # Példa sor: "CPU Power: 4.65 W"
                cpu_power = line.split(":")[1].strip().replace(" W", "")
            if "GPU Power" in line:
                gpu_power = line.split(":")[1].strip().replace(" W", "")

        return cpu_power, gpu_power

    except Exception as e:
        print(f"Hiba: {e}")
        return None, None

def main():
    # CSV fejléc létrehozása (ha új fájl)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_power_w", "gpu_power_w"])

    print(f"Adatok mentése ide: {OUTPUT_FILE} (CTRL+C-vel leállítható)")

    try:
        while True:
            timestamp = datetime.now().isoformat()
            cpu_power, gpu_power = get_metrics()

            if cpu_power and gpu_power:
                with open(OUTPUT_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, cpu_power, gpu_power])

                print(f"{timestamp} | CPU: {cpu_power} W | GPU: {gpu_power} W")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nLeállítva.")

def plot():
    # CSV fájl beolvasása
    df = pd.read_csv("metrics_log.csv")

    # Szöveges oszlopok tisztítása: "284 mW" → 284.0
    df["cpu_power_mw"] = df["cpu_power_w"].str.replace(" mW", "", regex=False).astype(float)
    df["gpu_power_mw"] = df["gpu_power_w"].str.replace(" mW", "", regex=False).astype(float)

    # Időbélyeg konvertálása datetime típusra
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["cpu_power_mw"], label="CPU Power (mW)", linewidth=2)
    plt.plot(df["timestamp"], df["gpu_power_mw"], label="GPU Power (mW)", linewidth=2)

    plt.xlabel("Idő")
    plt.ylabel("Teljesítmény (mW)")
    plt.title("CPU és GPU fogyasztás Apple Siliconon")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Időbélyegek szépen elforgatva
    plt.gcf().autofmt_xdate()

    plt.show()

if __name__ == "__main__":
    # main()
    plot()