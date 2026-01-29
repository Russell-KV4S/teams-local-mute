# AutoHotkey Teams Mute (Local API)

A lightweight, "blind" mute toggle for Microsoft Teams that works globally—even when Teams is minimized or in the background.

Unlike standard hotkeys (`Ctrl+Shift+M`), this tool uses the **Microsoft Teams Local API** (WebSockets). This means it works 100% of the time, regardless of which window is in focus, and it correctly updates your mute status icon in the Teams app.

## Why use this?
* **Reliability:** Standard hotkeys often fail if Teams isn't the active window. This script talks directly to the Teams backend.
* **State Aware:** It doesn't just cut your microphone audio (like a system mute); it actually toggles the mute function *inside* Teams.
* **Hardware Friendly:** Perfect for mapping to mouse buttons (Razer/Logitech) or macropads.

## Requirements
* [AutoHotkey v2](https://www.autohotkey.com/)
* [Python 3.x](https://www.python.org/downloads/)
* Python Websocket Library:
  ```bash
  pip install websocket-client
  ```
  
## Installation
1. Download this repository.
2. Ensure `TeamsMute.ahk` and `teams_toggle.py` are in the **same folder**.
3. **Enable the API in Teams:**
    * Open Microsoft Teams.
    * Go to **Settings > Privacy**.
    * Scroll down to **Third-party app API**.
    * Click **Manage API** and ensure **Enable API** is turned **ON**.

## Setup & First Run
1. Run the `TeamsMute.ahk` script.
2. Press the **Pause/Break** key on your keyboard (Default Hotkey).
3. **Look at Teams:** A popup will appear asking to allow "MuteScript" to connect.
4. Click **Allow**.

> **Note:** This is a one-time authorization. The script will save a `teams_token.txt` file locally.

## Customization
To change the hotkey, edit `TeamsMute.ahk` and change `Pause::` to whatever key you prefer (e.g., `F13`, `ScrollLock`, etc.).

## Troubleshooting
* **Script keeps asking for permission?** Delete `teams_token.txt` and try running the script again.
* **Nothing happens?** Check `error_log.txt` in the script folder for details.