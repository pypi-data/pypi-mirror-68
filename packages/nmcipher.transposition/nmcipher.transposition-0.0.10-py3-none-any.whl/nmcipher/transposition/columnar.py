class Columnar():

    @staticmethod
    def pad(string, length, padding=' '):
        return string if len(string) >= length else Columnar.pad(string + padding, length, padding)

    @staticmethod
    def core_algorithm(key, message):
        columns = tuple(Columnar.pad(message[i : i + key], key) for i in range(0, len(message), key))
        return ''.join(''.join(column[i] for column in columns) for i in range(key))

    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        return Columnar.core_algorithm(self.key, message)

    def decrypt(self, message):
        return Columnar.core_algorithm(len(message) // self.key if self.key != 0 else len(message), message).strip()
