from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/authorize')
def authorize():
    return "CORS is working!"

if __name__ == '__main__':
    app.run(port=4999, debug=True)