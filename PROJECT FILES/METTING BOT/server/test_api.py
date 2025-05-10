import requests

response = requests.post(
    "http://127.0.0.1:5000/transcribe",
    json={"meeting_url": "paste your url"}
)

print("Status Code:", response.status_code)
print("Response:", response.json())
