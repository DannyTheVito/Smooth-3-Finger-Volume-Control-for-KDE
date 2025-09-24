#!/usr/bin/env python3
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess

# ---------------------------
# Adjust this substring to match your touchpad
DEVICE_SUBSTRING = "Touchpad"
# Threshold to ignore small jitters
THRESHOLD = 2
# ---------------------------

def increase_volume():
    subprocess.run('qdbus org.kde.kglobalaccel /component/kmix invokeShortcut "increase_volume"', shell=True)

def decrease_volume():
    subprocess.run('qdbus org.kde.kglobalaccel /component/kmix invokeShortcut "decrease_volume"', shell=True)

# ---------------------------
# Detect touchpad device
devices = [InputDevice(path) for path in evdev.list_devices()]
dev = None
for d in devices:
    if DEVICE_SUBSTRING in d.name:
        dev = d
        break

if dev is None:
    print("Touchpad not found! Available devices:")
    for d in devices:
        print(f"{d.path}: {d.name}")
    exit(1)

print(f"Using touchpad device: {dev.path} ({dev.name})")

# ---------------------------
# Multi-touch tracking
active_slots = {}
current_slot = None
prev_avg_y = None

for event in dev.read_loop():
    if event.type != ecodes.EV_ABS:
        continue

    absevent = categorize(event)
    code = absevent.event.code
    val = absevent.event.value

    # Track current slot
    if code == ecodes.ABS_MT_SLOT:
        current_slot = val

    elif code == ecodes.ABS_MT_POSITION_Y:
        if current_slot is None:
            continue
        active_slots[current_slot] = (active_slots.get(current_slot, (0,0))[0], val)

        if len(active_slots) == 3:
            avg_y = sum(y for x,y in active_slots.values()) / 3
            if prev_avg_y is not None:
                delta = prev_avg_y - avg_y
                if abs(delta) >= THRESHOLD:
                    if delta > 0:
                        increase_volume()
                    else:
                        decrease_volume()
                    prev_avg_y = avg_y
            else:
                prev_avg_y = avg_y
        else:
            prev_avg_y = None

    elif code == ecodes.ABS_MT_TRACKING_ID:
        if val == -1:
            # Finger lifted
            if current_slot in active_slots:
                active_slots.pop(current_slot)
            if len(active_slots) < 3:
                prev_avg_y = None
