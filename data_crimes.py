#Sofia Mase
from flask import Flask, render_template, request, jsonify
import requests
import json  # Import the json module

app = Flask(__name__)

# Azure GeoData Service URL
geo_data_api_url = "https://azure.geodataservice.net/GeoDataService.svc/GetUSDemographics"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crimedata', methods=['GET'])
def get_crime_data():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        zipcode = request.args.get('zipcode')

        if not (latitude and longitude) and not zipcode:
            return jsonify({'error': 'Latitude and longitude or zipcode required'}), 400

        params = {
            'includecrimedata': 'true',
            'latitude': latitude,
            'longitude': longitude,
            'zipcode': zipcode
        }

        response = requests.get(geo_data_api_url, params=params)

        if response.status_code == 200:
            if response.text:
                try:
                    crime_data = response.json()
                    crime_count = crime_data.get('CrimeCount', 0)
                    return jsonify({'crime_count': crime_count})
                except json.JSONDecodeError:
                    return jsonify({'error': 'Invalid JSON response from the API'}), 500
            else:
                return jsonify({'error': 'Empty response from the API'}), 500
        else:
            return jsonify({'error': 'Failed to fetch crime data'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
