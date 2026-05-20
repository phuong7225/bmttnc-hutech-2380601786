class TranspositionCipher:
    def encrypt_text(self, text: str, key: int) -> str:
        if key <= 1 or key >= len(text):
            return text

        encrypted_text = [""] * key

        for column in range(key):
            pointer = column

            while pointer < len(text):
                encrypted_text[column] += text[pointer]
                pointer += key

        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        if key <= 1 or key >= len(text):
            return text

        num_columns = (len(text) + key - 1) // key
        num_rows = key
        num_shaded_boxes = (num_columns * num_rows) - len(text)
        decrypted_text = [""] * num_columns
        column = 0
        row = 0

        for letter in text:
            decrypted_text[column] += letter
            column += 1

            if column == num_columns or (
                column == num_columns - 1 and row >= num_rows - num_shaded_boxes
            ):
                column = 0
                row += 1

        return "".join(decrypted_text)
