import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.caesar import Ui_MainWindow


API_BASE_URL = "http://127.0.0.1:5000/api/caesar"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.Decrypt.clicked.connect(self.call_api_decrypt)

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def build_payload(self):
        key = self.ui.textEdit_2.toPlainText().strip()
        if not key:
            self.show_message("Missing key", "Please enter a Caesar key.", QMessageBox.Warning)
            return None

        payload = {
            "plain_text": self.ui.textEdit.toPlainText(),
            "key": key,
        }
        return payload

    def call_api(self, action, result_keys):
        payload = self.build_payload()
        if payload is None:
            return

        url = f"{API_BASE_URL}/{action}"
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            data = response.json()

            result = next((data[key] for key in result_keys if key in data), None)
            if result is None:
                raise KeyError(f"Response missing keys: {', '.join(result_keys)}")

            self.ui.textEdit_3.setText(result)
            self.show_message("Success", f"{action.capitalize()} successfully.")
        except requests.exceptions.RequestException as e:
            self.show_message("API error", str(e), QMessageBox.Critical)
        except (KeyError, ValueError) as e:
            self.show_message("Invalid response", str(e), QMessageBox.Critical)

    def call_api_encrypt(self):
        self.call_api("encrypt", ("encrypted_message", "Encrypted_message"))

    def call_api_decrypt(self):
        self.call_api(
            "decrypt",
            ("decrypted_message", "Decrypted_message", "encrypted_message"),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
