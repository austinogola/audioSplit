
from flask import Flask, request, jsonify, send_file
import os
from io import BytesIO
import requests
from pydub import AudioSegment
import shutil
from spleeter.separator import Separator
from werkzeug.utils import secure_filename
import time
from dotenv import load_dotenv
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import jwt
import wget
# from supabase_utils import (upload_audio_to_supabase,check_file_exists_in_bucket,download_file_from_bucket)
from functools import wraps
import threading
import datetime
import glob
from pydub.utils import mediainfo

app = Flask(__name__)
CORS(app)
load_dotenv()

separator = Separator('spleeter:2stems', multiprocess=False)

print("SEPARATOR",separator)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'separated'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/separate', methods=['POST'])
def separate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    base_name = os.path.splitext(filename)[0]
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_dir = os.path.join(OUTPUT_FOLDER, base_name)
    vocals_path = os.path.join(output_dir, 'vocals.mp3')
    start = time.time()
    # Save the uploaded file
    file.save(input_path)

    try:
        # Separate
        separator.separate_to_file(input_path, OUTPUT_FOLDER,codec="mp3", bitrate="128k")
        os.remove(input_path)
        end = time.time()

        print('FINISHED IN ',end-start)

        if not os.path.exists(vocals_path):
            return jsonify({'error': 'Vocals file not found after separation'}), 500

        # Return the vocals audio file
        return send_file(vocals_path, mimetype='audio/mpeg', as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/separate2', methods=['POST'])
def separate2():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    stems = request.form.get("stems", "2")   # default 2
    quality = request.form.get("quality", "standard")  # "standard" or "high"

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    base_name = os.path.splitext(filename)[0]
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_dir = os.path.join(OUTPUT_FOLDER, base_name)
    os.makedirs(output_dir, exist_ok=True)

    file.save(input_path)
    start = time.time()

    try:
        # configure separator (quality can map to model size)
        model = f"spleeter:{stems}stems"
        if quality == "high":
            model += "-hq"

        separator = Separator(model)
        separator.separate_to_file(input_path, OUTPUT_FOLDER, codec="mp3", bitrate="128k")

        os.remove(input_path)

        # Zip all stems
        zip_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for f in files:
                    zipf.write(os.path.join(root, f), f)

        end = time.time()
        print("FINISHED IN", end - start)

        return send_file(zip_path, mimetype="application/zip", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500