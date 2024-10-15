import os
from flask import Flask, render_template
from stega.Text.text import text


UPLOAD_IMAGE_FOLDER = 'stega/Image/static'
IMAGE_CACHE_FOLDER = 'stega/Image/__pycache__'
UPLOAD_TEXT_FOLDER = 'stega/Text/static'
TEXT_CACHE_FOLDER = 'stega/Text/__pycache__'


# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='./stega/Text/templates')
app.secret_key = "hello"
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['IMAGE_CACHE_FOLDER'] = IMAGE_CACHE_FOLDER
app.config['UPLOAD_TEXT_FOLDER'] = UPLOAD_TEXT_FOLDER
app.config['TEXT_CACHE_FOLDER'] = TEXT_CACHE_FOLDER
app.register_blueprint(text, url_prefix="/text")

@app.route("/")
@app.route('/text/encode')
def encode():
    return render_template('encode-text.html')

if __name__ == "__main__":
    app.run(debug=True)
