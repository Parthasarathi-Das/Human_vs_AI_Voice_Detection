import base64

audio_path = "input.mp3"
output_base64_file = "mp3_base64.txt"

def encode_audio(mp3_file_path):
    with open(mp3_file_path, "rb") as mp3_file:
        mp3_bytes = mp3_file.read()

    base64_bytes = base64.b64encode(mp3_bytes)
    base64_string = base64_bytes.decode("utf-8")
    print("MP3 successfully converted to Base64s")
    return base64_string

encoded_string = encode_audio("input1.mp3")
with open(output_base64_file, "w") as f:
    f.write(encoded_string)