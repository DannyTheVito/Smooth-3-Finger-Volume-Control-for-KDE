# Smooth-3-Finger-Volume-Control-for-KDE
A Python script to control volume on KDE Plasma using 3-finger swipes on your touchpad. Swipe up/down with three fingers to increase or decrease volume, and see the on-screen volume OSD.

---

## Features

* **Continuous 3-finger swipe up/down** → volume up/down
* **OSD shows** for every volume change (via KDE DBus shortcuts)
* Works on **X11 and Wayland**
* No `sudo` required — runs as a normal user

---

## Requirements

* KDE Plasma Desktop (X11 or Wayland)
* Python 3
* `evdev` Python module (Debian/Ubuntu: `python3-evdev`)
* User must be in the `input` group to read touchpad events

```bash
sudo usermod -aG input $USER
```

Log out and back in (or restart) for the group change to take effect. 
Confirm with ```groups```

---

## Installation

1. Clone or download this repository:

```bash
git clone https://github.com/yourusername/3finger-volume-kde.git
cd 3finger-volume-kde
```

2. Make the script executable:

```bash
chmod +x 3fingervolume_kde.py
```

3. Run the script:

```bash
python3 3fingervolume_kde.py
```

---

## Configuration

* **Touchpad detection:** By default, the script searches for any device containing `"Touchpad"` in its name.
* **Swipe sensitivity:** Adjust the `THRESHOLD` variable in the script to ignore small jitters.
* **Volume step:** Controlled by KDE System Settings → Audio → Volume step. The script uses DBus shortcuts, so the OSD reflects your KDE volume step.

---

## Autostart on Login (KDE)

To automatically run the script on login:

1. Open **System Settings → Startup and Shutdown → Autostart**
2. Click **Add Script** and select a small wrapper script:

```bash
#!/bin/bash
python3 /path/to/3fingervolume_kde.py &
```

3. Save and restart.

---

## Troubleshooting

* **Script cannot find touchpad:** Make sure your user is in the `input` group and logged out/in.
* **Volume steps too large:** Adjust KDE System Settings → Audio → Volume step.

---

## License

MIT License — feel free to modify and distribute.
