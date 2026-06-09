from flask import Flask, request, jsonify
from caesar import CaesarCipher
from vigenere import VigenereCipher
from railfence import RailFenceCipher
from playfair import PlayFairCipher
from transposition import TranspositionCipher

app = Flask(__name__)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plaint_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(plaint_text, key)
    return jsonify({'decrypted_message': decrypted_text})

@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.encrypt_text(plaint_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = data['key']
    decrypted_text = vigenere_cipher.decrypt_text(plaint_text, key)
    return jsonify({'decrypted_message': decrypted_text})

@app.route("/api/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = railfence_cipher.encrypt_text(plaint_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    decrypted_text = railfence_cipher.decrypt_text(plaint_text, key)
    return jsonify({'decrypted_message': decrypted_text})

@app.route("/api/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = data['key']
    encrypted_text = playfair_cipher.encrypt_text(plaint_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = data['key']
    decrypted_text = playfair_cipher.decrypt_text(plaint_text, key)
    return jsonify({'decrypted_message': decrypted_text})

@app.route("/api/playfair/creatematrix", methods=["POST"])
def playfair_creatematrix():
    data = request.json
    key = data['key']
    matrix = playfair_cipher.create_matrix(key)
    return jsonify({'matrix': matrix})

@app.route("/api/transposition/encrypt", methods=["POST"])
@app.route("/transposition/encrypt", methods=["POST"])
@app.route("/TRANSPOSITION/encrypt", methods=["POST"])
def transposition_encrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = transposition_cipher.encrypt_text(plaint_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/transposition/decrypt", methods=["POST"])
@app.route("/transposition/decrypt", methods=["POST"])
@app.route("/TRANSPOSITION/decrypt", methods=["POST"])
def transposition_decrypt():
    data = request.json
    plaint_text = data['plain_text']
    key = int(data['key'])
    decrypted_text = transposition_cipher.decrypt_text(plaint_text, key)
    return jsonify({'decrypted_message': decrypted_text})

#main funtion
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug = True)
