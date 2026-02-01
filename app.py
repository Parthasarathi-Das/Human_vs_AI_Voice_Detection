from flask import Flask, jsonify, request
from dotenv import load_dotenv
from base64decoder import validate_base64
import os
from voice_detector import get_prediction

load_dotenv("secret_key.env")
VALID_API_KEY = os.getenv("API_KEY")

REQUIRED_FIELDS = ["language", "audioFormat", "audioBase64"]
LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello API"

@app.route('/voice-detection', methods=['POST'])
def myFun():
    '''
        At first validating the request to prevent error in core steps
    '''
    api_key = request.headers.get("x-api-key")

    if not api_key:
        return throw_error("API key is required in x-api-key header"), 400
    
    if api_key != VALID_API_KEY:
        return throw_error("Invalid API key"), 401
    
    data = request.get_json(silent=True)
    
    if data is None:
        return throw_error("Malformed Request"), 400
    
    
    for field in REQUIRED_FIELDS:
        if field not in data:
            return  throw_error(f"Missing required field: {field}"), 400
    

    if data["language"] not in LANGUAGES:
        return throw_error("Only Tamil, English, Hindi, Malayalam, Telugu languages are supported"), 400
    
    if data["audioFormat"] !="mp3":
        return throw_error("Only mp3 format is supported"), 400
    
    corrupted = not validate_base64(data["audioBase64"])
    if corrupted:
        return throw_error("Corrupted encoding of audio"), 400
    
    '''
        Utilizing prediction of model
    '''

    label, conf, explanation = get_prediction(data["language"])

    # If all validations pass
    return throw_success(data["language"], label, conf, explanation), 200

def throw_error(message):
    return jsonify({
        "status" : "error",
        "message": message
    })

def throw_success(language, prediction, confidence, explanation):
    return jsonify({
        "status" : "success",
        "language" : language,
        "classification": prediction,
        "confidenceScore": confidence,
	    "explanation": explanation
    })

if(__name__ == "__main__"):

    app.run(debug=True, host="0.0.0.0", port=5000)
