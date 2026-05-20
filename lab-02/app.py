from flask import Flask, render_template, request

from cipher.caesar import CaesarCipher


app = Flask(__name__)
caesar_cipher = CaesarCipher()


def transform_caesar_text(text: str, key: int, action: str) -> str:
    output_text = []

    for letter in text:
        if letter.upper() in caesar_cipher.alphabet:
            if action == "decrypt":
                output_text.append(caesar_cipher.decrypt_text(letter, key))
            else:
                output_text.append(caesar_cipher.encrypt_text(letter, key))
        else:
            output_text.append(letter)

    return "".join(output_text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/caesar", methods=["GET", "POST"])
def caesar():
    result = ""
    error = ""
    text = ""
    key = 3
    action = "encrypt"

    if request.method == "POST":
        text = request.form.get("text", "")
        key_text = request.form.get("key", "3")
        action = request.form.get("action", "encrypt")

        try:
            key = int(key_text)
            result = transform_caesar_text(text, key, action)
        except ValueError:
            error = "Key must be a number."

    return render_template(
        "caesar.html",
        result=result,
        error=error,
        text=text,
        key=key,
        action=action,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
