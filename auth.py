import os
import base64

def getConfig():
    configPath = os.path.join(
        os.getenv("LOCALAPPDATA"),
        R"Riot Games\Riot Client\Config\lockfile"
    )

    try:
        with open(configPath) as lockfile:
            data = lockfile.read().split(":")
            keys = ["name", "PID", "port", "password", "protocol"]
            return dict(zip(keys, data))
    except Exception:
        raise RuntimeError("bruh lockfile err")

def getHeaders():
    config = getConfig()
    accessToken = base64.b64encode(
        ("riot:" + config["password"]).encode()).decode()
    headers = {
        "Authorization": f"Basic {accessToken}",
        "User-Agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows; 10;;Professional, x64)"
    }
    return headers
