import base64
import binascii
import argparse
import os
import sys
from pathlib import Path

import rsa


class RSACipher:
    def __init__(self, key_dir=None):
        self.key_dir = Path(key_dir) if key_dir else Path(__file__).resolve().parent / "key"
        self.private_key_path = self.key_dir / "private_key.pem"
        self.public_key_path = self.key_dir / "public_key.pem"
        self.key_dir.mkdir(parents=True, exist_ok=True)

    def generate_keys(self, key_size=1024):
        key_size = int(key_size)
        if key_size < 512:
            raise ValueError("Key size must be at least 512 bits.")

        public_key, private_key = rsa.newkeys(key_size)

        self.public_key_path.write_bytes(public_key.save_pkcs1("PEM"))
        self.private_key_path.write_bytes(private_key.save_pkcs1("PEM"))

        return public_key, private_key

    def load_public_key(self):
        self.ensure_keys()
        return rsa.PublicKey.load_pkcs1(self.public_key_path.read_bytes())

    def load_private_key(self):
        self.ensure_keys()
        return rsa.PrivateKey.load_pkcs1(self.private_key_path.read_bytes())

    def ensure_keys(self):
        if not self.public_key_path.exists() or not self.private_key_path.exists():
            self.generate_keys()

    def encrypt(self, message):
        public_key = self.load_public_key()
        message_bytes = message.encode("utf-8")
        chunk_size = rsa.common.byte_size(public_key.n) - 11
        encrypted_chunks = []

        for index in range(0, len(message_bytes), chunk_size):
            chunk = message_bytes[index:index + chunk_size]
            encrypted_chunks.append(rsa.encrypt(chunk, public_key))

        encrypted_data = b"".join(encrypted_chunks)
        return base64.b64encode(encrypted_data).decode("ascii")

    def decrypt(self, encrypted_message):
        private_key = self.load_private_key()
        try:
            encrypted_data = base64.b64decode(encrypted_message, validate=True)
        except binascii.Error as exc:
            raise ValueError("Invalid Base64 encrypted message.") from exc

        chunk_size = rsa.common.byte_size(private_key.n)
        decrypted_chunks = []

        if len(encrypted_data) % chunk_size != 0:
            raise ValueError("Invalid encrypted message.")

        for index in range(0, len(encrypted_data), chunk_size):
            chunk = encrypted_data[index:index + chunk_size]
            try:
                decrypted_chunks.append(rsa.decrypt(chunk, private_key))
            except rsa.pkcs1.DecryptionError as exc:
                raise ValueError("Cannot decrypt message with the current private key.") from exc

        return b"".join(decrypted_chunks).decode("utf-8")

    def sign(self, message, hash_method="SHA-256"):
        private_key = self.load_private_key()
        signature = rsa.sign(message.encode("utf-8"), private_key, hash_method)
        return base64.b64encode(signature).decode("ascii")

    def verify(self, message, signature):
        public_key = self.load_public_key()

        try:
            signature_bytes = base64.b64decode(signature, validate=True)
        except binascii.Error as exc:
            raise ValueError("Invalid Base64 signature.") from exc

        try:
            hash_method = rsa.verify(message.encode("utf-8"), signature_bytes, public_key)
        except rsa.pkcs1.VerificationError:
            return False, None

        return True, hash_method


def run_cli(argv=None):
    parser = argparse.ArgumentParser(description="RSA cipher demo")
    parser.add_argument("--message", default="Xin chao RSA", help="Message to encrypt and sign")
    parser.add_argument("--key-size", type=int, default=1024, help="RSA key size in bits")
    args = parser.parse_args(argv)

    cipher = RSACipher()
    cipher.generate_keys(args.key_size)

    encrypted_message = cipher.encrypt(args.message)
    decrypted_message = cipher.decrypt(encrypted_message)
    signature = cipher.sign(args.message)
    verified, hash_method = cipher.verify(args.message, signature)

    print("RSA demo completed")
    print(f"Public key: {cipher.public_key_path}")
    print(f"Private key: {cipher.private_key_path}")
    print(f"Plain text: {args.message}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}")
    print(f"Signature: {signature}")
    print(f"Verified: {verified}")
    print(f"Hash method: {hash_method}")


def run_gui(argv=None):
    project_root = Path(__file__).resolve().parents[2]
    platforms_dir = project_root / "platforms"

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    if platforms_dir.exists():
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", str(platforms_dir))

    from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
    from ui.rsa import Ui_MainWindow

    class RSAWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.cipher = RSACipher()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle("RSA Cipher")

            self.ui.btn_encrypt.setText("Encrypt")
            self.ui.txt_plaint_text.setAcceptRichText(False)
            self.ui.txt_cipher_text.setAcceptRichText(False)
            self.ui.txt_info.setAcceptRichText(False)
            self.ui.txt_sign.setAcceptRichText(False)

            self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
            self.ui.btn_encrypt.clicked.connect(self.encrypt)
            self.ui.btn_decrypt.clicked.connect(self.decrypt)
            self.ui.btn_sign.clicked.connect(self.sign)
            self.ui.btn_verify.clicked.connect(self.verify)

        def show_message(self, title, text, icon=QMessageBox.Information):
            msg = QMessageBox(self)
            msg.setIcon(icon)
            msg.setWindowTitle(title)
            msg.setText(text)
            msg.exec_()

        def set_info(self, text):
            self.ui.txt_info.setText(text)

        def generate_keys(self):
            try:
                public_key, _ = self.cipher.generate_keys()
                key_size = public_key.n.bit_length()
                self.set_info(
                    f"Generated {key_size}-bit keys.\n"
                    f"Public key: {self.cipher.public_key_path}\n"
                    f"Private key: {self.cipher.private_key_path}"
                )
                self.show_message("Success", "Keys generated successfully.")
            except ValueError as exc:
                self.show_message("Generate keys error", str(exc), QMessageBox.Critical)

        def encrypt(self):
            plain_text = self.ui.txt_plaint_text.toPlainText()
            if not plain_text:
                self.show_message("Missing text", "Please enter plain text.", QMessageBox.Warning)
                return

            try:
                encrypted_message = self.cipher.encrypt(plain_text)
                self.ui.txt_cipher_text.setText(encrypted_message)
                self.set_info("Encrypted successfully.")
            except ValueError as exc:
                self.show_message("Encrypt error", str(exc), QMessageBox.Critical)

        def decrypt(self):
            encrypted_message = self.ui.txt_cipher_text.toPlainText().strip()
            if not encrypted_message:
                self.show_message("Missing text", "Please enter cipher text.", QMessageBox.Warning)
                return

            try:
                decrypted_message = self.cipher.decrypt(encrypted_message)
                self.ui.txt_plaint_text.setText(decrypted_message)
                self.set_info("Decrypted successfully.")
            except ValueError as exc:
                self.show_message("Decrypt error", str(exc), QMessageBox.Critical)

        def sign(self):
            plain_text = self.ui.txt_plaint_text.toPlainText()
            if not plain_text:
                self.show_message("Missing text", "Please enter plain text.", QMessageBox.Warning)
                return

            try:
                signature = self.cipher.sign(plain_text)
                self.ui.txt_sign.setText(signature)
                self.set_info("Signed successfully.")
            except ValueError as exc:
                self.show_message("Sign error", str(exc), QMessageBox.Critical)

        def verify(self):
            plain_text = self.ui.txt_plaint_text.toPlainText()
            signature = self.ui.txt_sign.toPlainText().strip()

            if not plain_text:
                self.show_message("Missing text", "Please enter plain text.", QMessageBox.Warning)
                return

            if not signature:
                self.show_message("Missing signature", "Please enter signature.", QMessageBox.Warning)
                return

            try:
                verified, hash_method = self.cipher.verify(plain_text, signature)
            except ValueError as exc:
                self.show_message("Verify error", str(exc), QMessageBox.Critical)
                return

            if verified:
                self.show_message("Verify", "verified Successfully")
            else:
                self.show_message("Verify", "Verified Fail", QMessageBox.Warning)

    app = QApplication([sys.argv[0], *(argv or [])])
    window = RSAWindow()
    window.show()
    return app.exec_()


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cli_flags = ("--cli", "--message", "--key-size")
    use_cli = any(arg in cli_flags or arg.startswith("--message=") or arg.startswith("--key-size=") for arg in argv)

    if use_cli:
        argv = [arg for arg in argv if arg != "--cli"]
        run_cli(argv)
        return

    sys.exit(run_gui(argv))


if __name__ == "__main__":
    main()
