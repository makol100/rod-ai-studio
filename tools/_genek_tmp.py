import os, time, requests, json, base64

API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6I-uChfnArm9RHFMgj-BjChYvhg5ky7TmWKvjKIP0KyHg")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Convert k5_krok2.png to jpeg
os.system("ffmpeg -y -i data/remont_wc/k5_krok2.png -vframes 1 -q:v 2 data/remont_wc/k5_krok2.jpg 2>/dev/null")

with open("data/remont_wc/k5_krok2.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "instances": [{
        "prompt": "Small bathroom, perfectly flat white painted wall above the tiles, flat white suspended ceiling, white rimless wall-hung ceramic toilet bowl under the black flush plate. Natural lighting. Handheld camera, very slow movement.",
        "image": {
            "bytesBase64Encoded": img_b64,
            "mimeType": "image/jpeg"
        }
    }],
    "parameters": {
        "durationSeconds": 4,
        "resolution": "720p",
        "aspectRatio": "9:16"
    }
}

print("Starting generation on veo-3.1-fast-generate-preview...", flush=True)
url = f"{BASE_URL}/models/veo-3.1-fast-generate-preview:predictLongRunning?key={API_KEY}"
r = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
if r.status_code != 200:
    print(r.status_code, r.text)
    exit(1)

op_name = r.json().get("name")
print("Operation:", op_name, flush=True)

for i in range(30):
    time.sleep(10)
    op_url = f"{BASE_URL}/{op_name}?key={API_KEY}"
    r_stat = requests.get(op_url)
    stat_data = r_stat.json()
    if stat_data.get("done"):
        print("Done!", flush=True)
        try:
            uri = stat_data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
            print("URI:", uri)
            video_data = requests.get(f"{uri}?key={API_KEY}").content
            with open("data/remont_wc/veo_test.mp4", "wb") as f:
                f.write(video_data)
            print("Saved to veo_test.mp4")
        except Exception as e:
            print("Error parsing final video:", stat_data, e)
        break
    else:
        print("Waiting...", flush=True)
