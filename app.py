from flask import Flask
from flask import render_template
import os
import sys

'''
La idea es recibir en los args el path de la ubicación de las fotos y decirle a la aplicación
que vaya a buscar las fotos a ese lugar

'''
path = sys.argv[1]
app = Flask(__name__)



@app.route('/')
def index():
    images = ['/static/' + name for name in os.listdir(str(path)) if name.endswith(".jpg") or name.endswith(".png")]
    # render_template va a buscar a la carpeta 'templates' por default
    return render_template('index.html', images=images)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=False)
    app.run(debug=True)
