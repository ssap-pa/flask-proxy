from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAZBNYwM-f35rAAWbHQv76jOGuiE3txpSU'

@app.route('/places', methods=['GET'])
def get_places():
    location = request.args.get('location')
    radius = request.args.get('radius', 500)
    type_ = request.args.get('type', 'restaurant')

    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={location}&radius={radius}&type={type_}&key={GOOGLE_API_KEY}"
    )
    res = requests.get(url)
    return jsonify(res.json())
