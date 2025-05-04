from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/pollution-data', methods=['GET'])
def get_pollution_data():
    city = request.args.get('city')
    country = request.args.get('country')

    if not city or not country:
        return jsonify({'error': 'Missing city or country parameter'}), 400

    url = f'https://www.numbeo.com/pollution/in/{city}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            # WHO pollution table
            who_table = soup.find('table', {'class': 'who_pollution_data_widget'})
            who_rows = who_table.find_all('tr')

            pm10 = who_rows[1].find_all('td')[1].text.strip()
            pm2_5 = who_rows[2].find_all('td')[1].text.strip()
            pm10_pollution_level = who_rows[3].find('span', {'class': 'pollution_level'}).text.strip()

            # Pollution Index table
            index_table = soup.find('table', {'class': 'table_indices'})
            index_rows = index_table.find_all('tr')

            pollution_index = index_rows[1].find_all('td')[1].text.strip()
            pollution_exp_scale = index_rows[2].find_all('td')[1].text.strip()

            return jsonify({
                'city': city,
                'country': country,
                'pm10': pm10,
                'pm2_5': pm2_5,
                'pm10_pollution_level': pm10_pollution_level,
                'pollution_index': pollution_index,
                'pollution_exp_scale': pollution_exp_scale
            })

        except AttributeError as e:
            return jsonify({
                'error': 'Unable to find the required data on the page.',
                'message': str(e)
            }), 500

    else:
        return jsonify({'error': f'Failed to retrieve data, status code: {response.status_code}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
