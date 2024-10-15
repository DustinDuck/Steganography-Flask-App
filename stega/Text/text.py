import os
from PIL import Image
import stepic
import shutil
from flask import Blueprint, current_app, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
# from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad


text = Blueprint("stega", __name__, static_folder="static",
                 template_folder="templates")


@text.route("/encode")
def text_encode():
    if os.path.exists(current_app.config['TEXT_CACHE_FOLDER']):
        shutil.rmtree(
            current_app.config['TEXT_CACHE_FOLDER'], ignore_errors=False)
    else:
        print("Not Found")

    if os.path.exists(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png")):
        # print("Found")
        os.remove(os.path.join(
            current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png"))
    else:
        print("Not found")
    return render_template("encode-text.html", active_page='encode')


@text.route("/encode-result", methods=['POST', 'GET'])
def text_encode_result():
    if request.method == 'POST':
        message = request.form['message']
        encryption_type = request.form['encryption_type']
        if 'text_file' in request.files:
            text_file = request.files['text_file']
            if text_file and text_file.filename != '':
                message = text_file.read().decode('utf-8')

        if 'image_file' not in request.files:
            flash('No image found')
        image_file = request.files['image_file']

        if image_file.filename == '':
            flash('No image selected')

        if image_file:
            print(message)
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename))
            text_encryption = True
            key = encrypt_text(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename), message)
            print(key)
        else:
            text_encryption = False
        result = request.form

        return render_template("encode-text-result.html", result=result, image_file=image_file, text_encryption=text_encryption, message=message, key=key)


@text.route("/decode")
def text_decode():
    return render_template("decode-text.html", active_page='decode')


@text.route("/decode-result", methods=['POST', 'GET'])
def text_decode_result():
    if request.method == 'POST':
        key = request.form['key']
        if 'image_file' not in request.files:
            flash('No image found')
        image_file = request.files['image_file']
        if image_file.filename == '':
            flash('No image selected')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename))
            text_decryption = True
            message = decrypt_text(os.path.join(
                current_app.config['UPLOAD_TEXT_FOLDER'], filename), key)
            message = unpad(message, AES.block_size).decode()
        else:
            text_decryption = False
        result = request.form
        return render_template("decode-text-result.html", result=result, image_file=image_file, text_decryption=text_decryption, message=message)



def encrypt_text(image_1, message, encryption_type):
    im = Image.open(image_1)

    key = get_random_bytes(16)
    key_hex = key.hex()

    if encryption_type == "AES":
        cipher = AES.new(key, AES.MODE_ECB)
    elif encryption_type == "3DES":
        cipher = DES3.new(key, DES3.MODE_ECB)
    else:
        raise ValueError("Invalid encryption type")

    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)

    message = encrypted_message.hex()

    im1 = stepic.encode(im, bytes(str(message), encoding='utf-8'))
    im1.save(os.path.join(
        current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png"))
    return key_hex

def decrypt_text(image_1, key_hex, encryption_type):
    print(key_hex)
    im2 = Image.open(image_1)
    stegoImage = stepic.decode(im2)

    if encryption_type == "AES":
        cipher = AES.new(bytes.fromhex(key_hex), AES.MODE_ECB)
    elif encryption_type == "3DES":
        cipher = DES3.new(bytes.fromhex(key_hex), DES3.MODE_ECB)
    else:
        raise ValueError("Invalid encryption type")
    print("cipher:", cipher)
    # fetch the encrypted message from the stego image
    encrypted_message = bytes.fromhex(stegoImage)
    # decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message
