class Caesar():

    @staticmethod
    def translate_symbols(key, symbols, reverse=False):
        table = {symbols[i]: symbols[(i + key) % len(symbols)] for i in range(len(symbols))}
        return str.maketrans(table if not reverse else {v: k for k, v in table.items()})

    def __init__(self, key, symbols):
        self._translation_table = self.translate_symbols(key, symbols)
        self._reverse_translation_table = self.translate_symbols(key, symbols, True)

    def encrypt(self, message):
        return message.translate(self._translation_table)

    def decrypt(self, message):
        return message.translate(self._reverse_translation_table)
