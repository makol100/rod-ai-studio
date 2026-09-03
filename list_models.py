import urllib.request
import json
import os

key = "rc_59fa0a2f6bd0f3138268d0c3ede435e0a781bcdad85d5f0ef69760bca26f61f5"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        for m in data.get("models", []):
            print(m.get("name"))
except Exception as e:
    print(f"Error: {e}")
