from flask import Flask, redirect, url_for, session, jsonify, request
from authlib.integrations.flask_client import OAuth
from bson import ObjectId
import datetime
import jwt
import os
from flask_cors import CORS
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


json_data = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
if not json_data:
    raise Exception("Service account JSON not found in environment")

creds_dict = json.loads(json_data)

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# 
# CREDS_FILE = "creds.json"  # Your downloaded service account key


        
SPREADSHEET_NAME = "Muteify Email List"  # Your Google Sheet name

SPREADSHEET_ID = 0



# Authorize gspread
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1  # Access the first sheet

app = Flask(__name__)
CORS(app)


app.config["MONGO_URI"] = os.getenv("MONGO_DB_URL")
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route('/auth/google',methods=["POST"])
def google_auth():
    users = mongo.db.users
    accounts = mongo.db.accounts
    data = request.json
    
    code = data.get("code")
    scope = data.get("scope")
    origin = data.get("origin")
    
    print(code)
    print(origin)
    
    token_url = 'https://oauth2.googleapis.com/token'
    
    token_response = req.post(token_url, data={
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': f'{origin}/oauth-google',
        'grant_type': 'authorization_code',
    }).json()
  
    
    access_token = token_response.get('access_token')
    expires_in = token_response.get('expires_in')  # in seconds
    id_token_jwt = token_response.get('id_token')  # JWT token
    
    idinfo = id_token.verify_oauth2_token(id_token_jwt, requests.Request(), GOOGLE_CLIENT_ID)
    email = idinfo.get('email')
    
    if email:
        token = ''
        user = users.find_one({"email": email})
        if user:
            token = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=21)}, SECRET_KEY, algorithm="HS256") 
        else:
            user_result = users.insert_one({"email": email,"plan":"Trial"})
            user_id = str(user_result.inserted_id)
            accounts.insert_one({
                "userId": user_id,
                "usage": [],
                "payments": [],
                "plan": "Trial"  # Default to "Trial" plan
            })
            token = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=21)}, SECRET_KEY, algorithm="HS256")
            
        return jsonify({"token": token,"success":True,"error":False})
    else:
        return jsonify({"error": "No email found"}), 401
    
    




@app.route("/signup", methods=["POST"])
def signup():
    
    users = mongo.db.users
    accounts = mongo.db.accounts
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email":email}):
        return jsonify({"error": "User with email  already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user_result = users.insert_one({"email": email, "password": hashed_pw,"plan":"Trial"})
    print(user_result)
    user_id = str(user_result.inserted_id)
    accounts.insert_one({
        "userId": user_id,
        "usage": [],
        "payments": [],
        "plan": "Trial"  # Default to "Trial" plan
    })
    token = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=21)}, SECRET_KEY, algorithm="HS256")
    return jsonify({"message": "User created successfully","success":True,"error":False,"token":token}), 201

@app.route("/login", methods=["POST"])
def login():
    users = mongo.db.users
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = users.find_one({"email": email})

    if user:
        if bcrypt.check_password_hash(user["password"], password):
            token = jwt.encode({
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=21)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({"token": token,"success":True,"error":False})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "No user with this email"}), 401
    
    
    
@app.route('/submit-email', methods=['POST'])
def submit_email():
    data = request.get_json()
    email = data.get('email')
    
    print(email)

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        sheet.append_row([email])
        return jsonify({"message": "Email added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)