from flask import Flask
from flask import render_template
import os


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def hello_world():
    images = os.listdir("static/images")
    return render_template('index.html', images=images)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=False)
    app.run(debug=True)
