import json
import time
import random
import datetime

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def generate_telemetry(machine):
    # Simulate variations around a baseline
    temp = machine["baseline_temp"] + random.uniform(-2.0, 5.0)
    vibration = machine["baseline_vibration"] + random.uniform(-0.5, 1.5)
    
    return {
        "machine_id": machine["id"],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "temperature": round(temp, 2),
        "vibration": round(vibration, 2),
        "rpm": random.randint(1400, 1600),
        "current": round(random.uniform(9.0, 15.0), 2),
        "status": "RUNNING"
    }

def main():
    config = load_config()
    print(f"Starting simulation. Sending data to {config['backend_url']}")
    
    while True:
        for machine in config["machines"]:
            telemetry = generate_telemetry(machine)
            print(f"Generated telemetry for {machine['id']}: {telemetry}")
            # TODO: Add HTTP POST to backend here using requests library
            
        time.sleep(config["simulation_interval_seconds"])

if __name__ == "__main__":
    main()
