from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAZBNYwM-f35rAAWbHQv76jOGuiE3txpSU'  # 실제 키로 교체

def geocode_location(location):
    """주소(텍스트) → 위경도 변환"""
    geocode_url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={location}&key={GOOGLE_API_KEY}"
    )
    response = requests.get(geocode_url)
    result = response.json()
    if result['status'] == 'OK' and result['results']:
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
        return f"{lat},{lng}"
    return None

@app.route('/places', methods=['GET'])
def get_places():
    location = request.args.get('location')
    radius = request.args.get('radius', 500)
    type_ = request.args.get('type', 'restaurant')

    # location이 위경도 좌표가 아니면 자동 변환
    if location and not (',' in location and all(x.replace('.', '', 1).replace('-', '', 1).isdigit() for x in location.split(','))):
        geocoded = geocode_location(location)
        if geocoded is None:
            return jsonify({"results": [], "status": "INVALID_LOCATION"}), 400
        location = geocoded

    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={location}&radius={radius}&type={type_}&key={GOOGLE_API_KEY}"
    )

    res = requests.get(url)
    return jsonify(res.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
