import urllib.request, urllib.error, json

data = json.dumps({
    "name": "Neel",
    "phone": "1234567891",
    "concern": "kh",
    "preferredDate": "2026-01-30"
}).encode()

req = urllib.request.Request(
    "http://localhost:8000/api/bookings/create-guest",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("STATUS:", resp.status)
        print("BODY:", resp.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("BODY:", e.read().decode())
except Exception as e:
    print("ERROR:", str(e))
