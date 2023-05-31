from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    with open('alllocdata.json', 'r') as f:
        data = json.load(f)

    # Convert date strings to datetime objects, sort, then convert back to strings
    for item in data['data']:
        item['date'] = datetime.strptime(item['date'], '%a %b %d %Y %H:%M:%S')

    data['data'].sort(key=lambda x: x['date'], reverse=True)

    for item in data['data']:
        item['date'] = item['date'].strftime('%a %b %d %Y %H:%M:%S')

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", threaded=True)
