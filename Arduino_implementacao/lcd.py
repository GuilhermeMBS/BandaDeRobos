import json, serial, time
from datetime import datetime

with open("timeline.json", "r", encoding="utf-8") as f:
    timeline = json.load(f)

ser = serial.Serial("COM15", 9600)
start_time = datetime.now()

for entry in timeline:
    target = entry["start"]
    verse = entry["verse"]

    while (datetime.now() - start_time).total_seconds() < target:
        time.sleep(0.01)

    ser.write(('$' + verse + '\n').encode())
    print(f"Sent at {target:.2f}s: {verse}")