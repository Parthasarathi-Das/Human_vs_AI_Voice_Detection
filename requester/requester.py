import requests
from base64encoder import encode_audio

#API_URL = "http://127.0.0.1:5000/voice-detection"
API_URL = "https://partha-sarathi-voicedetection.hf.space/voice-detection"
API_KEY = "gdchxdfhxyrfhxcyc"
AUDIO_FILE = "input5.mp3"   # path to your audio file
LANGUAGE = "Hindi"
AUDIO_FORMAT = "mp3"


audio_base64 = encode_audio(AUDIO_FILE)

payload = {
    "language": LANGUAGE,
    "audioFormat": AUDIO_FORMAT,
    "audioBase64": audio_base64
}

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

response = requests.post(
    API_URL,
    json=payload,
    headers=headers,
    timeout=120
)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except Exception:
    print("Raw Response:", response.text)
