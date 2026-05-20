from string import ascii_uppercase


class PlayFairCipher:
    def __init__(self):
        self.alphabet = ascii_uppercase.replace("J", "")

    def create_matrix(self, key: str) -> list[list[str]]:
        key = self.clean_text(key)
        matrix_letters = []

        for letter in key + self.alphabet:
            if letter not in matrix_letters:
                matrix_letters.append(letter)

        return [
            matrix_letters[index:index + 5]
            for index in range(0, len(matrix_letters), 5)
        ]

    def clean_text(self, text: str) -> str:
        text = text.upper().replace("J", "I")
        return "".join(letter for letter in text if letter in ascii_uppercase)

    def prepare_text(self, text: str) -> list[str]:
        text = self.clean_text(text)
        pairs = []
        index = 0

        while index < len(text):
            first_letter = text[index]

            if index + 1 >= len(text):
                second_letter = "Z" if first_letter != "Z" else "X"
                index += 1
            else:
                second_letter = text[index + 1]

                if first_letter == second_letter:
                    second_letter = "X" if first_letter != "X" else "Q"
                    index += 1
                else:
                    index += 2

            pairs.append(first_letter + second_letter)

        return pairs

    def find_position(self, matrix: list[list[str]], letter: str) -> tuple[int, int]:
        for row_index, row in enumerate(matrix):
            if letter in row:
                return row_index, row.index(letter)

        return -1, -1

    def encrypt_text(self, text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        encrypted_text = []

        for pair in self.prepare_text(text):
            row1, col1 = self.find_position(matrix, pair[0])
            row2, col2 = self.find_position(matrix, pair[1])

            if row1 == row2:
                encrypted_text.append(matrix[row1][(col1 + 1) % 5])
                encrypted_text.append(matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:
                encrypted_text.append(matrix[(row1 + 1) % 5][col1])
                encrypted_text.append(matrix[(row2 + 1) % 5][col2])
            else:
                encrypted_text.append(matrix[row1][col2])
                encrypted_text.append(matrix[row2][col1])

        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        text = self.clean_text(text)
        decrypted_text = []

        for index in range(0, len(text), 2):
            pair = text[index:index + 2]

            if len(pair) < 2:
                pair += "X"

            row1, col1 = self.find_position(matrix, pair[0])
            row2, col2 = self.find_position(matrix, pair[1])

            if row1 == row2:
                decrypted_text.append(matrix[row1][(col1 - 1) % 5])
                decrypted_text.append(matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                decrypted_text.append(matrix[(row1 - 1) % 5][col1])
                decrypted_text.append(matrix[(row2 - 1) % 5][col2])
            else:
                decrypted_text.append(matrix[row1][col2])
                decrypted_text.append(matrix[row2][col1])

        return "".join(decrypted_text)
