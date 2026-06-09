from flask import Flask, jsonify, request

from cipher.ecc import ECCCipher
from cipher.rsa import RSACipher


app = Flask(__name__)
rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()


def get_json_payload():
    return request.get_json(silent=True) or {}


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Cipher API",
            "routes": [
                "/api/rsa/generate_keys",
                "/api/rsa/encrypt",
                "/api/rsa/decrypt",
                "/api/rsa/sign",
                "/api/rsa/verify",
                "/api/ecc/generate_keys",
                "/api/ecc/sign",
                "/api/ecc/verify",
            ],
        }
    )


@app.route("/api/rsa/generate-keys", methods=["GET", "POST"])
@app.route("/api/rsa/generate_keys", methods=["GET", "POST"])
def generate_keys():
    data = get_json_payload()
    key_size_value = request.args.get("key_size", data.get("key_size", 1024))

    try:
        key_size = int(key_size_value)
        rsa_cipher.generate_keys(key_size)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "message": "Keys generated successfully.",
            "key_size": key_size,
        }
    )


@app.route("/api/rsa/encrypt", methods=["POST"])
def encrypt():
    data = get_json_payload()
    plain_text = data.get("plain_text", data.get("message", ""))

    if not plain_text:
        return jsonify({"error": "plain_text is required."}), 400

    try:
        encrypted_message = rsa_cipher.encrypt(plain_text)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"encrypted_message": encrypted_message})


@app.route("/api/rsa/decrypt", methods=["POST"])
def decrypt():
    data = get_json_payload()
    encrypted_message = data.get("encrypted_message", data.get("cipher_text", ""))

    if not encrypted_message:
        return jsonify({"error": "encrypted_message is required."}), 400

    try:
        decrypted_message = rsa_cipher.decrypt(encrypted_message)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"decrypted_message": decrypted_message})


@app.route("/api/rsa/sign", methods=["POST"])
def sign():
    data = get_json_payload()
    plain_text = data.get("plain_text", data.get("message", ""))
    hash_method = data.get("hash_method", "SHA-256")

    if not plain_text:
        return jsonify({"error": "plain_text is required."}), 400

    try:
        signature = rsa_cipher.sign(plain_text, hash_method)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "signature": signature,
        }
    )


@app.route("/api/rsa/verify", methods=["POST"])
@app.route("/api/rsa/verifyrifiy", methods=["POST"])
@app.route("/api/rsa/verifiy", methods=["POST"])
def verify():
    data = get_json_payload()
    plain_text = data.get("plain_text", data.get("message", ""))
    signature = data.get("signature", "")

    if not plain_text:
        return jsonify({"error": "plain_text is required."}), 400

    if not signature:
        return jsonify({"error": "signature is required."}), 400

    try:
        verified, hash_method = rsa_cipher.verify(plain_text, signature)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "is_verified": verified,
        }
    )


@app.route("/api/ecc/generate-keys", methods=["GET", "POST"])
@app.route("/api/ecc/generate_keys", methods=["GET", "POST"])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({"message": "ECC keys generated successfully."})


@app.route("/api/ecc/sign", methods=["POST"])
def ecc_sign():
    data = get_json_payload()
    information = data.get("information", data.get("plain_text", data.get("message", "")))

    if not information:
        return jsonify({"error": "information is required."}), 400

    signature = ecc_cipher.sign(information)
    return jsonify({"signature": signature})


@app.route("/api/ecc/verify", methods=["POST"])
def ecc_verify():
    data = get_json_payload()
    information = data.get("information", data.get("plain_text", data.get("message", "")))
    signature = data.get("signature", "")

    if not information:
        return jsonify({"error": "information is required."}), 400

    if not signature:
        return jsonify({"error": "signature is required."}), 400

    try:
        verified = ecc_cipher.verify(information, signature)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"is_verified": verified})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
