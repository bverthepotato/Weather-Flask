from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

key = 'ad692a690a08dd3442799002941b95a6'
API_ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def weather_detector():
    if request.method == 'POST':
        location = request.form['location']
        if location:
            params = {
                'q': location,
                'appid': key,
                'units': 'metric'
            }
            response = requests.get(API_ENDPOINT, params=params)
            data = response.json()

            if response.status_code == 200:
                city = data['name']
                country = data['sys']['country']
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                wind_speed = data['wind']['speed']
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'city': city,
                        'country': country,
                        'temperature': temperature,
                        'description': description,
                        'wind_speed': wind_speed
                    })

                return render_template('index.html', city=city, country=country, temperature=temperature,
                                       description=description, wind_speed=wind_speed)

            else:
                error_message = data.get('message', 'Unknown error')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error_message': error_message}), 400
                return render_template('index.html', error_message=error_message)

    error_message = request.args.get('error_message')
    if error_message:
        return render_template('index.html', error_message=error_message)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error_message': 'Invalid request'}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
