import argparse
import base64
import binascii
import hashlib
import os
import sys
from pathlib import Path

from ecdsa import BadSignatureError, NIST256p, SigningKey, VerifyingKey


class ECCCipher:
    def __init__(self, key_dir=None):
        self.key_dir = Path(key_dir) if key_dir else Path(__file__).resolve().parent / "keys"
        self.private_key_path = self.key_dir / "private_key.pem"
        self.public_key_path = self.key_dir / "public_key.pem"
        self.key_dir.mkdir(parents=True, exist_ok=True)

    def generate_keys(self):
        private_key = SigningKey.generate(curve=NIST256p, hashfunc=hashlib.sha256)
        public_key = private_key.get_verifying_key()

        self.private_key_path.write_bytes(private_key.to_pem())
        self.public_key_path.write_bytes(public_key.to_pem())

        return public_key, private_key

    def ensure_keys(self):
        if not self.public_key_path.exists() or not self.private_key_path.exists():
            self.generate_keys()

    def load_private_key(self):
        self.ensure_keys()
        return SigningKey.from_pem(self.private_key_path.read_bytes(), hashfunc=hashlib.sha256)

    def load_public_key(self):
        self.ensure_keys()
        return VerifyingKey.from_pem(self.public_key_path.read_bytes())

    def sign(self, message):
        private_key = self.load_private_key()
        signature = private_key.sign_deterministic(
            message.encode("utf-8"),
            hashfunc=hashlib.sha256,
        )
        return base64.b64encode(signature).decode("ascii")

    def verify(self, message, signature):
        public_key = self.load_public_key()

        try:
            signature_bytes = base64.b64decode(signature, validate=True)
        except binascii.Error as exc:
            raise ValueError("Invalid Base64 signature.") from exc

        try:
            return public_key.verify(
                signature_bytes,
                message.encode("utf-8"),
                hashfunc=hashlib.sha256,
            )
        except BadSignatureError:
            return False


def run_cli(argv=None):
    parser = argparse.ArgumentParser(description="ECC signature demo")
    parser.add_argument("--message", default="Xin chao ECC", help="Message to sign and verify")
    args = parser.parse_args(argv)

    cipher = ECCCipher()
    cipher.generate_keys()

    signature = cipher.sign(args.message)
    verified = cipher.verify(args.message, signature)

    print("ECC demo completed")
    print(f"Public key: {cipher.public_key_path}")
    print(f"Private key: {cipher.private_key_path}")
    print(f"Information: {args.message}")
    print(f"Signature: {signature}")
    print(f"Verified: {verified}")


def run_gui(argv=None):
    project_root = Path(__file__).resolve().parents[2]
    platforms_dir = project_root / "platforms"

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    if platforms_dir.exists():
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", str(platforms_dir))

    from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
    from ui.ecc import Ui_MainWindow

    class ECCWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.cipher = ECCCipher()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle("ECC Cipher")

            self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
            self.ui.btn_sign.clicked.connect(self.sign)
            self.ui.btn_verify.clicked.connect(self.verify)

        def show_message(self, title, text, icon=QMessageBox.Information):
            msg = QMessageBox(self)
            msg.setIcon(icon)
            msg.setWindowTitle(title)
            msg.setText(text)
            msg.exec_()

        def generate_keys(self):
            self.cipher.generate_keys()
            self.show_message("Success", "Keys generated successfully.")

        def sign(self):
            information = self.ui.txt_info.toPlainText()
            if not information:
                self.show_message("Missing information", "Please enter information.", QMessageBox.Warning)
                return

            signature = self.cipher.sign(information)
            self.ui.txt_sign.setPlainText(signature)
            self.show_message("Success", "Signed successfully.")

        def verify(self):
            information = self.ui.txt_info.toPlainText()
            signature = self.ui.txt_sign.toPlainText().strip()

            if not information:
                self.show_message("Missing information", "Please enter information.", QMessageBox.Warning)
                return

            if not signature:
                self.show_message("Missing signature", "Please enter signature.", QMessageBox.Warning)
                return

            try:
                verified = self.cipher.verify(information, signature)
            except ValueError as exc:
                self.show_message("Verify error", str(exc), QMessageBox.Critical)
                return

            if verified:
                self.show_message("Verify", "verified Successfully")
            else:
                self.show_message("Verify", "Verified Fail", QMessageBox.Warning)

    app = QApplication([sys.argv[0], *(argv or [])])
    window = ECCWindow()
    window.show()
    return app.exec_()


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    use_cli = "--cli" in argv or any(arg.startswith("--message") for arg in argv)

    if use_cli:
        argv = [arg for arg in argv if arg != "--cli"]
        run_cli(argv)
        return

    sys.exit(run_gui(argv))


if __name__ == "__main__":
    main()
