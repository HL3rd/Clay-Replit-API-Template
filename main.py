import os
import json
import requests
import time

from functools import wraps
from replit import db
from flask import Flask, jsonify, request

app = Flask('app')

# Wrapper function to add API endpoint security
# Generate your own API key, save it in Secrets as "INTERNAL_API_KEY"
# All requests will need to include this string in the "Authorization" header
def require_api_key(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    api_key = request.headers.get('Authorization')
    if api_key and api_key == os.environ.get('INTERNAL_API_KEY'):
      return f(*args, **kwargs)
    else:
      return jsonify({"error": "Unauthorized"}), 401
  return decorated_function

# API endpoint that wraps around a Clay Webhook Tabe
@app.route('/clay/api-start', methods=['POST'])
@require_api_key
def clay_api_start():
  try:
    request_data = request.get_json()
    print('--- REQ CLAY API START', json.dumps(request_data))

    # Generate a unique ID for this request
    request_id = str(int(time.time() * 1000))
    
    # Write the request id to the database
    db[request_id] = None

    # Send the request to the Clay Table
    clay_url = os.environ['CLAY_TABLE_WEBHOOK_URL']

    # Payload
    data = {
      "data": request_data
    }
    
    clay_resp = requests.post(clay_url, json=data)
    if clay_resp.status_code != 200:
      del db[request_id]
      return jsonify({"error": f"Clay API call failed {clay_resp.json()}"}), 400

    # Wait for the email status in db to written to
    # or timeout after 5 minutes
    start_time = time.time()
    while True:
      time.sleep(1)
      if db[request_id] or time.time() - start_time > 300:
        print(f"Request {request_id} updated in db or function timed out")
        break

    # Once data is written, grab the response data
    json_string_resp = db[request_id]

    if json_string_resp:
      # Convert it back into JSON object
      json_resp = json.loads(json_string_resp)
      del db[request_id]
      return jsonify(json_resp), 200
    else:
      del db[request_id]
      return jsonify({
        "message": f"No Clay data found for request: {request_id}",
      }), 200
  except Exception as e:
    return jsonify({"error": f"Error in /clay/api-start: {e}" }), 500

@app.route('/clay/api-complete', methods=['POST'])
@require_api_key
def clay_api_complete():
  try:
    request_data = request.get_json()
    print('--- REQ CLAY API COMPLETE', json.dumps(request_data, indent=2))
    request_id = request_data.get('request_id')
    
    # Write the whole response as a JSON string in the key-value store
    # This will end the "listener" at /api-start endpoint
    db[request_id] = json.dumps(request_data)
    
    return jsonify(request_data), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500

app.run(host='0.0.0.0', port=8080)