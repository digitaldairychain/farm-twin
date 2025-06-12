"""Adaptor to pull data from Decentlabs and push to farm-twin API."""

import concurrent.futures
import datetime
import json

import requests

MW = 1000

config = {}
devices = {}


def get_measurements(device, sensor, start, end):
    """Fetch sensor measurements for a given device sensor."""
    q_string = (
        """SELECT value FROM "measurements" WHERE node =~ /^"""
        + device
        + """$/ AND sensor =~ /^"""
        + sensor
        + """$/ AND time >= '"""
        + start.isoformat()
        + """Z' AND time <= '"""
        + end.isoformat()
        + """Z'"""
    )
    data = query_db(q_string)["results"][0]["series"][0]["values"]
    write_data(device, sensor, start, data)


def get_measurements_async(start, end):
    """Fetch measurement data asynchronously.
    Each thread pulls the measurements for a single device between two times.
    """
    for device in devices.items():
        with concurrent.futures.ThreadPoolExecutor(max_workers=MW) as executor:
            _ = {
                executor.submit(get_measurements, device[0], sensor, start, end): sensor
                for sensor in device[1]
            }


def get_sensors(device):
    """Fetch all attached sensors for a given device.
    Store this for future queries.
    """
    data = query_db(
        "SHOW TAG VALUES WITH KEY = sensor WHERE node =~ /^"
        + device
        + "$/ AND channel !~ /^link-/"
    )
    sensors = data["results"][0]["series"][0]["values"]
    for sensor in sensors:
        devices[device][sensor[1]] = {}


def get_sensors_async():
    """Fetch attached sensor data asynchronously.
    Each thread pulls the sensors for a single device.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=MW) as executor:
        _ = {executor.submit(get_sensors, device): device for device in devices}


def query_db(query):
    """Send a query to the remote Decentlab API."""
    request = requests.get(
        config["url"],
        params={"db": "main", "epoch": "ms", "q": query},
        headers={"Authorization": f"Bearer {config['api_key']}"},
        timeout=10,
    )
    data = json.loads(request.text)
    return data


def load_config():
    """Load config.json with runtime parameters."""
    with open("config.json", encoding="utf-8") as f:
        _config = json.load(f)
        f.close()
    _config["url"] = (
        f"https://{_config['domain']}/api/datasources/"
        f"proxy/uid/{_config['database']}/query"
    )
    _config["end_date"] = datetime.datetime.strptime(_config["end_date"], "%d/%m/%Y")
    try:
        _config["start_date"] = datetime.datetime.strptime(
            _config["start_date"], "%d/%m/%Y"
        )
    except KeyError:
        _config["start_date"] = datetime.datetime.now()
    return _config


def call_api(body, dp):
    """POST data to farm-twin API."""
    body["timestamp"] = dp[0]
    body["value"] = dp[1]
    requests.post("http://localhost:8000/features/data/", json=body)


def write_data(device, sensor, date, data):
    """A0synchronously write data to farm-twin API."""
    body = {"device": device, "sensor": sensor}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MW) as executor:
        _ = {executor.submit(call_api, body, dp): dp for dp in data}


def create_devices():
    """Create and initialise device dictionary."""
    for device in config["devices"]:
        devices[device] = {}


if __name__ == "__main__":
    config = load_config()
    create_devices()
    get_sensors_async()
    get_measurements_async(config["start_date"], config["end_date"])
