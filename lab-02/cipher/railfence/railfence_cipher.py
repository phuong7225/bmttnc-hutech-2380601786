class RailFenceCipher:
    def encrypt_text(self, text: str, key: int) -> str:
        if key <= 1 or key >= len(text):
            return text

        rails = [""] * key
        rail = 0
        direction = 1

        for letter in text:
            rails[rail] += letter

            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1

            rail += direction

        return "".join(rails)

    def decrypt_text(self, text: str, key: int) -> str:
        if key <= 1 or key >= len(text):
            return text

        pattern = []
        rail = 0
        direction = 1

        for _ in text:
            pattern.append(rail)

            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1

            rail += direction

        rail_lengths = [pattern.count(rail_index) for rail_index in range(key)]
        rails = []
        start = 0

        for length in rail_lengths:
            rails.append(list(text[start:start + length]))
            start += length

        decrypted_text = []

        for rail_index in pattern:
            decrypted_text.append(rails[rail_index].pop(0))

        return "".join(decrypted_text)
