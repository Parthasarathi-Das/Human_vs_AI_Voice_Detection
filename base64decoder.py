import base64
import binascii

input_base64_file = "mp3_base64.txt"
decoded_mp3_file = "temp.mp3"

def validate_base64(base64_string:str):
    try:
        mp3_bytes = base64.b64decode(base64_string, validate=True)

        if len(mp3_bytes) == 0:
            raise ValueError("Decoded data is empty")

        with open(decoded_mp3_file, "wb") as mp3:
            mp3.write(mp3_bytes)

        print("Base64 successfully converted back to MP3")
        return True
    except binascii.Error:
        print("Invalid Base64 string (corrupted or illegal characters)")
        return False

    except ValueError as e:
        print(f"Error: {e}")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
# with open(input_base64_file, "r") as f:
#     audiostr = f.read()
# validate_base64(audiostr)