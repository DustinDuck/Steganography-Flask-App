import os
from flask import Flask, render_template
from stega.Text.text import text


UPLOAD_IMAGE_FOLDER = 'modes/Image/static'
IMAGE_CACHE_FOLDER = 'modes/Image/__pycache__'
UPLOAD_TEXT_FOLDER = 'modes/Text/static'
TEXT_CACHE_FOLDER = 'modes/Text/__pycache__'
UPLOAD_AUDIO_FOLDER = 'modes/Audio/static'
AUDIO_CACHE_FOLDER = 'modes/Audio/__pycache__'
UPLOAD_VIDEO_FOLDER = 'modes/Video/static'
VIDEO_CACHE_FOLDER = 'modes/Video/__pycache__'


# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='./modes/Text/templates')
app.secret_key = "hello"
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['IMAGE_CACHE_FOLDER'] = IMAGE_CACHE_FOLDER
app.config['UPLOAD_TEXT_FOLDER'] = UPLOAD_TEXT_FOLDER
app.config['TEXT_CACHE_FOLDER'] = TEXT_CACHE_FOLDER
app.config['UPLOAD_AUDIO_FOLDER'] = UPLOAD_AUDIO_FOLDER
app.config['AUDIO_CACHE_FOLDER'] = AUDIO_CACHE_FOLDER
app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER
app.config['VIDEO_CACHE_FOLDER'] = VIDEO_CACHE_FOLDER
app.register_blueprint(text, url_prefix="/text")

@app.route("/")
@app.route('/text/encode')
def encode():
    return render_template('encode-text.html')

if __name__ == "__main__":
    app.run(debug=True)
