from flask import Flask, render_template, redirect, url_for,request
from flask_cors import CORS, cross_origin
from flask import make_response
from index import obtainData
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/data', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'GET':
        resultado = obtainData()
        return resultado

if __name__ == "__main__":
    app.run(debug = True)