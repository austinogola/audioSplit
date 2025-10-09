from flask import Flask, request, jsonify, send_file, send_from_directory
from spleeter.separator import Separator
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os, threading, time, zipfile, uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'separated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

jobs = {}  # track job progress and results


def process_file(job_id, input_path, output_dir, stems, quality):
    try:
        jobs[job_id]["status"] = "processing"
        model = f"spleeter:{stems}stems"
        if quality == "high":
            model += "-hq"

        separator = Separator(model)
        separator.separate_to_file(input_path, OUTPUT_FOLDER, codec="mp3", bitrate="128k")
        os.remove(input_path)

        # Collect all stems
        stem_files = [
            os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".mp3")
        ]

        # Zip them
        zip_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in stem_files:
                zipf.write(file, os.path.basename(file))

        jobs[job_id]["status"] = "done"
        jobs[job_id]["files"] = [os.path.basename(f) for f in stem_files]
        jobs[job_id]["zip"] = os.path.basename(zip_path)

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


@app.route("/separate", methods=["POST"])
def separate():
    print('sEPARATING')
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    stems = request.form.get("stems", "2")
    quality = request.form.get("quality", "standard")

    filename = secure_filename(file.filename)
    job_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_dir = os.path.join(OUTPUT_FOLDER, job_id)
    os.makedirs(output_dir, exist_ok=True)

    file.save(input_path)

    jobs[job_id] = {"status": "uploaded", "progress": 0}

    threading.Thread(target=process_file, args=(job_id, input_path, output_dir, stems, quality)).start()

    return jsonify({"jobId": job_id})


@app.route("/progress/<job_id>")
def progress(job_id):
    job = jobs.get(job_id)
    print(job)
    if not job:
        return jsonify({"error": "Invalid job id"}), 404
    return jsonify(job)


@app.route("/results/<job_id>/<filename>")
def get_stem(job_id, filename):
    directory = os.path.join(OUTPUT_FOLDER, job_id)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/results/<job_id>/zip")
def get_zip(job_id):
    zip_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.zip")
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return jsonify({"error": "ZIP not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
