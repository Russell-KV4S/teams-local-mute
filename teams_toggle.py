import websocket
import json
import os
import time
import threading

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
# Get the absolute path of the folder where this script is running.
# This ensures it works on any computer, regardless of install location.
script_dir = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(script_dir, "teams_token.txt")
ERROR_LOG = os.path.join(script_dir, "error_log.txt")

# The local Teams API URL (Standard for all Teams installations)
URL_TEMPLATE = "ws://127.0.0.1:8124/?manufacturer=AHK&device=PC&app=MuteToggle&app-version=1.0&protocol-version=2.0.0&token={}"

def load_token():
    """Reads the authentication token from the local file if it exists."""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        except:
            return ""
    return ""

def save_token(token):
    """Saves the new token to disk so we don't have to re-authorize."""
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
            f.flush() # Ensure data is written immediately
            os.fsync(f.fileno()) # Force write to disk (prevents corruption)
    except Exception as e:
        log_error(f"Failed to save token: {e}")

def log_error(msg):
    """Simple logging for debugging issues on other users' machines."""
    try:
        with open(ERROR_LOG, "a") as f:
            f.write(f"{msg}\n")
    except:
        pass

def on_message(ws, message):
    data = json.loads(message)
    
    # Capture the token if Teams sends a refresh (happens on first connect)
    if "tokenRefresh" in data:
        save_token(data["tokenRefresh"])
        # Now that we have the token, we can close the connection safely
        ws.close()

def on_open(ws):
    # Send the Toggle Mute Command
    payload = {
        "action": "toggle-mute",
        "parameters": {},
        "requestId": 1
    }
    ws.send(json.dumps(payload))
    
    # INTELLIGENT CLOSING LOGIC:
    # If we already have a token file, we don't need to wait around.
    # If we DON'T have a token file, we must stay open so the user can click "Allow".
    if os.path.exists(TOKEN_FILE) and os.path.getsize(TOKEN_FILE) > 0:
        # We have a token, give it a moment to process the command, then kill it.
        def close_later():
            time.sleep(0.5)
            ws.close()
        threading.Thread(target=close_later).start()
    else:
        print("Waiting for user to click 'Allow' in Teams...")

def on_error(ws, error):
    # Only log real errors, ignore standard close interruptions
    if str(error) and "NoneType" not in str(error):
        log_error(f"Socket Error: {error}")

if __name__ == "__main__":
    current_token = load_token()
    ws_url = URL_TEMPLATE.format(current_token)
    
    # Connect to Teams
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()