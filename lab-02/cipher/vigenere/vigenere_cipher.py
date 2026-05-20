from string import ascii_uppercase


class VigenereCipher:
    def __init__(self):
        self.alphabet = list(ascii_uppercase)

    def generate_key(self, text: str, key: str) -> str:
        key = key.upper()
        key_length = len(key)
        generated_key = []

        for index in range(len(text)):
            generated_key.append(key[index % key_length])

        return "".join(generated_key)

    def encrypt_text(self, text: str, key: str) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        key = self.generate_key(text, key)
        encrypted_text = []

        for index, letter in enumerate(text):
            letter_index = self.alphabet.index(letter)
            key_index = self.alphabet.index(key[index])
            output_index = (letter_index + key_index) % alphabet_len
            output_letter = self.alphabet[output_index]
            encrypted_text.append(output_letter)

        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: str) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        key = self.generate_key(text, key)
        decrypted_text = []

        for index, letter in enumerate(text):
            letter_index = self.alphabet.index(letter)
            key_index = self.alphabet.index(key[index])
            output_index = (letter_index - key_index) % alphabet_len
            output_letter = self.alphabet[output_index]
            decrypted_text.append(output_letter)

        return "".join(decrypted_text)
