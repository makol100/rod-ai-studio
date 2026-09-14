import os, requests
key = os.environ.get('GEMINI_API_KEY', 'AQ.Ab8RN6I-uChfnArm9RHFMgj-BjChYvhg5ky7TmWKvjKIP0KyHg')
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
r = requests.get(url)
if r.status_code == 200:
    print([m['name'] for m in r.json().get('models', []) if 'vision' in m['name'] or 'gemini-1.5' in m['name'] or 'gemini-2' in m['name']])
else:
    print(r.status_code, r.text)
