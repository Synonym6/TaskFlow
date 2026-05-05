# Local Network Access

TaskFlow can be opened from a phone, tablet or another laptop in the same home Wi-Fi network as your PC.

## Current local IPv4

Active Wi-Fi adapter IPv4 on this PC:

- `192.168.0.20`

If your router gives the PC a new IP later, update `ALLOWED_HOSTS` in `taskflow/settings.py`.

## How to check the IP on Windows

Run:

```powershell
ipconfig
```

Find the active Wi-Fi adapter and copy the `IPv4 Address` value.

Example:

```text
Wireless LAN adapter Беспроводная сеть:
   IPv4 Address. . . . . . . . . . . : 192.168.0.20
```

## How to run TaskFlow for devices in the same Wi-Fi

1. Connect the PC and the phone to the same Wi-Fi network.
2. Make sure your current Wi-Fi IPv4 is listed in `ALLOWED_HOSTS`.
3. Start the Django server so it listens on all local interfaces:

```powershell
python manage.py runserver 0.0.0.0:8000
```

4. Open the site from another device:

```text
http://192.168.0.20:8000/
```

## Diagnostics

If the site does not open from the phone:

- the phone and the PC are not connected to the same Wi-Fi network;
- Windows Firewall is blocking port `8000`;
- Python or Django was not allowed on private networks;
- the PC IP address changed after reconnecting to Wi-Fi;
- the server was started on `127.0.0.1:8000` instead of `0.0.0.0:8000`;
- the current local IP is missing from `ALLOWED_HOSTS`.
